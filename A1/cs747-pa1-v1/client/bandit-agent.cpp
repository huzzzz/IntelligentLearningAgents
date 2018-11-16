#include <iostream>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <math.h>
#include <vector>
#include <random>
#include <string>

#include "gsl/gsl_rng.h"
#include "gsl/gsl_randist.h"

#define MAXHOSTNAME 256
#define INF 1e8

using namespace std;

void options(){

  cout << "Usage:\n";
  cout << "bandit-agent\n"; 
  cout << "\t[--numArms numArms]\n";
  cout << "\t[--randomSeed randomSeed]\n";
  cout << "\t[--horizon horizon]\n";
  cout << "\t[--hostname hostname]\n";
  cout << "\t[--port port]\n";
  cout << "\t[--algorithm algorithm]\n";
  cout << "\t[--epsilon epsilon]\n";

}


/*
  Read command line arguments, and set the ones that are passed (the others remain default.)
*/
bool setRunParameters(int argc, char *argv[], int &numArms, int &randomSeed, unsigned long int &horizon, string &hostname, int &port, string &algorithm, double &epsilon){

  int ctr = 1;
  while(ctr < argc){

    //cout << string(argv[ctr]) << "\n";

    if(string(argv[ctr]) == "--help"){
      return false;//This should print options and exit.
    }
    else if(string(argv[ctr]) == "--numArms"){
      if(ctr == (argc - 1)){
	return false;
      }
      numArms = atoi(string(argv[ctr + 1]).c_str());
      ctr++;
    }
    else if(string(argv[ctr]) == "--randomSeed"){
      if(ctr == (argc - 1)){
	return false;
      }
      randomSeed = atoi(string(argv[ctr + 1]).c_str());
      ctr++;
    }
    else if(string(argv[ctr]) == "--horizon"){
      if(ctr == (argc - 1)){
	return false;
      }
      horizon = atoi(string(argv[ctr + 1]).c_str());
      ctr++;
    }
    else if(string(argv[ctr]) == "--hostname"){
      if(ctr == (argc - 1)){
	return false;
      }
      hostname = string(argv[ctr + 1]);
      ctr++;
    }
    else if(string(argv[ctr]) == "--port"){
      if(ctr == (argc - 1)){
	return false;
      }
      port = atoi(string(argv[ctr + 1]).c_str());
      ctr++;
    }
    else if(string(argv[ctr]) == "--algorithm"){
      if(ctr == (argc - 1)){
  return false;
      }
      algorithm = string(argv[ctr + 1]);
      ctr++;
    }
     else if(string(argv[ctr]) == "--epsilon"){
      if(ctr == (argc - 1)){
  return false;
      }
      epsilon = atof(string(argv[ctr + 1]).c_str());
      ctr++;
    }
    else{
      return false;
    }

    ctr++;
  }

  return true;
}

double avg(double sum, unsigned long int pulls){
  if (pulls == 0){
    return 0;
  }
  return (double)(sum / pulls);
}

double ucb(double sum, unsigned long int pulls, unsigned long int totPulls){
  if (pulls == 0){
    return 0;
  }
  return (double)((sum / pulls) + sqrt(2 * log(totPulls) / pulls));
}

double kl_divergence(double p, double q)	{
	if (p == q){
		return 0;
	}
	else if(q == 0 || q == 1){
		return INF;
	}
	return (p * log(p/q) + (1-p)*log((1-p) / (1-q)));
}

double klucb(double sum, unsigned long int pulls, unsigned long int totPulls){
  if (pulls == 0){
    return 0;
  }
  double p_hat = avg(sum, pulls);
  double l = p_hat;
  double u = 1;
  double q = (l + u) / 2;
  while(l < u && u - l > 1e6){
  	q = (l + u) / 2;
  	if (pulls * kl_divergence(p_hat, q) <= (log(totPulls))){
  		l = q;
  	}
  	else{
  		u = q;
  	}
  }
  return q;
}

/* ============================================================================= */
/* Write your algorithms here */
int sampleArm(string algorithm, double epsilon, int pulls, float reward, int numArms, gsl_rng * r, double * sumRewards, unsigned long int * numPulls, unsigned long int * succ){
  int armToPull;
  if(algorithm.compare("rr") == 0){
    return(pulls % numArms);
  }
  
  else if(algorithm.compare("epsilon-greedy") == 0){
    double u = gsl_rng_uniform (r);
    
    if (u < epsilon){
      armToPull = (int)gsl_rng_uniform_int(r, numArms);
      // cout<<"Exploring"<<endl;
    }	
    else{
      int maxAvgRewardArm = 0;
      for (int i = 1; i < numArms; i++){
        if (avg(sumRewards[i], numPulls[i]) > avg(sumRewards[maxAvgRewardArm], numPulls[maxAvgRewardArm])){
          maxAvgRewardArm = i;
        }
      }
      armToPull = maxAvgRewardArm;
      // cout<<"Exploiting"<<endl;
    }
    return(armToPull);
  }
  else if(algorithm.compare("UCB") == 0){
    if (pulls < numArms){
      return(pulls % numArms);  
    }
    else{
      int maxUcbArm = 0;
      for (int i = 1; i < numArms; i++){
        if (ucb(sumRewards[i], numPulls[i], pulls) > ucb(sumRewards[maxUcbArm], numPulls[maxUcbArm], pulls)){
          maxUcbArm = i;
        }
      }
      armToPull = maxUcbArm;
      return(armToPull);
    }
  }
  else if(algorithm.compare("KL-UCB") == 0){
    if (pulls < numArms){
      return(pulls % numArms);  
    }
    else{
      int maxKLUcbArm = 0;
      for (int i = 1; i < numArms; i++){
        if (klucb(sumRewards[i], numPulls[i], pulls) > klucb(sumRewards[maxKLUcbArm], numPulls[maxKLUcbArm], pulls)){
          maxKLUcbArm = i;
        }
      }
      armToPull = maxKLUcbArm;
      return(armToPull); 
    }
    return(pulls % numArms);
  }
  else if(algorithm.compare("Thompson-Sampling") == 0){
  	double alpha = 1;
  	double beta = 1;

  	int maxtheteaArm = 0;
  	double max_theta = 0;
  	for (int i = 1; i < numArms; i++){
	    double curr_theta = gsl_ran_beta(r, alpha + succ[i], beta + numPulls[i] - succ[i]);
	    if (curr_theta > max_theta){
	    	max_theta = curr_theta;
	    	maxtheteaArm = i;
	    }
  	}

	armToPull = maxtheteaArm;
	return(armToPull);
  }
  else{
    return -1;
  }
}

/* ============================================================================= */

int main(int argc, char *argv[]){
  // Run Parameter defaults.
  int numArms = 5;
  int randomSeed = time(0);
  unsigned long int horizon = 200;
  string hostname = "localhost";
  int port = 5000;
  string algorithm="random";
  double epsilon=0.0;

  //Set from command line, if any.
  if(!(setRunParameters(argc, argv, numArms, randomSeed, horizon, hostname, port, algorithm, epsilon))){
    //Error parsing command line.
    options();
    return 1;
  }

  struct sockaddr_in remoteSocketInfo;
  struct hostent *hPtr;
  int socketHandle;

  bzero(&remoteSocketInfo, sizeof(sockaddr_in));
  
  if((hPtr = gethostbyname((char*)(hostname.c_str()))) == NULL){
    cerr << "System DNS name resolution not configured properly." << "\n";
    cerr << "Error number: " << ECONNREFUSED << "\n";
    exit(EXIT_FAILURE);
  }

  if((socketHandle = socket(AF_INET, SOCK_STREAM, 0)) < 0){
    close(socketHandle);
    exit(EXIT_FAILURE);
  }

  memcpy((char *)&remoteSocketInfo.sin_addr, hPtr->h_addr, hPtr->h_length);
  remoteSocketInfo.sin_family = AF_INET;
  remoteSocketInfo.sin_port = htons((u_short)port);

  if(connect(socketHandle, (struct sockaddr *)&remoteSocketInfo, sizeof(sockaddr_in)) < 0){
    //code added
    cout<<"connection problem"<<".\n";
    close(socketHandle);
    exit(EXIT_FAILURE);
  }

  // Random Num gen for epsilon greedy
 
  gsl_rng* r = gsl_rng_alloc(gsl_rng_mt19937);
  gsl_rng_set(r, randomSeed);

  // Setting up vectors for Sum so far and the number of pulls so far
  unsigned long int numPulls[numArms];
  unsigned long int succ[numArms];

  double sumRewards[numArms];

  for (int i=0; i < numArms; i++){
    sumRewards[i] = 0;
    numPulls[i] = 0;
    succ[i] = 0;
  }

  char sendBuf[256];
  char recvBuf[256];

  float reward = 0;
  unsigned long int pulls=0;
  int armToPull = sampleArm(algorithm, epsilon, pulls, reward, numArms, r, sumRewards, numPulls, succ);
  
  sprintf(sendBuf, "%d", armToPull);

  cout << "Sending action " << armToPull << ".\n";
  while(send(socketHandle, sendBuf, strlen(sendBuf)+1, MSG_NOSIGNAL) >= 0){

    char temp;
    recv(socketHandle, recvBuf, 256, 0);
    sscanf(recvBuf, "%f %c %lu", &reward, &temp, &pulls);
    cout << "Received reward " << reward << ".\n";
    cout<<"Num of  pulls "<<pulls<<".\n";
    
    sumRewards[armToPull] += reward;
    numPulls[armToPull] += 1;

    if (gsl_ran_bernoulli(r,reward)){
    	succ[armToPull] += 1;
    }

    armToPull = sampleArm(algorithm, epsilon, pulls, reward, numArms, r, sumRewards, numPulls, succ);

    sprintf(sendBuf, "%d", armToPull);
    cout << "Sending action " << armToPull << ".\n";
  }
  
  gsl_rng_free (r);

  close(socketHandle);

  cout << "Terminating.\n";

  return 0;
}
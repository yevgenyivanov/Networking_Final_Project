# Python Script README

This README file provides an overview of a Python script designed to analyze network packet data and generate various types of graphs. The script utilizes the Scapy library for network packet processing, pandas for data manipulation, numpy for numerical computations, and matplotlib for graph generation. The script reads data from CSV files containing network packet information and generates PDF function graphs, Inter-Message-Delay (IMD) graphs, and Complementary Cumulative Distribution Function (CCDF) graphs.

## Prerequisites

Before using the Python script, ensure you have the following prerequisites:

1. Python 3.x installed.
2. Required libraries: scapy, pandas, numpy, and matplotlib. You can install them using the following command:

```bash
pip install scapy pandas numpy matplotlib
```
3. Placed .csv files inside the ```resources/csvs/``` directory
## How to use
To use the Python script, follow these steps:

1. Download or clone the repository to your local machine.
2. Open a terminal and navigate to the downloaded folder.
3. Run the following command to execute the script:
```bash
python ./src/main.py
```
4. To see the generated graphs, check the ```results/``` folder

## Graph Generation
The script generates the following types of graphs from interpreted CSV files:

- PDF Function Graph
The PDF (Probability Density Function) function graph displays the probability density of inter-message delays within network packet data.

- Inter-Message-Delay (IMD) Graph
The IMD graph represents packet length over time intervals, providing insights into network traffic patterns.

- Complementary Cumulative Distribution Function (CCDF) Graph
The CCDF graph illustrates the complementary cumulative distribution of normalized message sizes, helping analyze message size distribution.

## Notes
 - Please ensure that all columns required by the script's methods are present and correctly named in the CSV files used for analysis. The script depends on specific column names for accurate graph generation.
 - The script deletes *all* files and directories that may be present in the ```results/``` folder. If you need to make any backups, move the files to a different, *external* directory.

## Explained Examples

#### CASE 1
this is the case where the attacked user is always active in (at most) a single IM group
there are two stages for this case - one without noise (i.e, while capturing packets of whatsapp in wireshark, there is no other website that is used) , and one with noise (i.e, while capturing packets of whatsapp in wireshark, we are using Spotify in the background).

## without noise

### for each IM group , we focused on two graphs:
1. fig. 2 in paper - graph that shows how the packet lengths changes over time, when time (in seconds) is the period where the group was monitored by the attacker (one of us), while the users of the group made communication (each group has its own communication). notice that in this case, we monitor each group seperately.
   
2. fig. 3 in paper graph that shows the distribution of Inter Message Delays, represented along the x-axis in seconds. x-axis: Inter Message Delay (imd) is the difference in time between sequencial messages. y-axis: indicates the likelihood of observing specific Inter Message Delays within certain intervals.


and for all the groups, we have a graph that shows the Complementary Cumulative Distribution Function (CCDF) for normalized message size distributions across various message types (fig. 4): distinct lines or curves on the graph correspond to different message types, allowing for a comparative analysis of their IM Size distributions.

according to the definition of CCDF, the curve depicts the probability that an IM Size (normalized message size) of the group (this is the random variable x) is bigger than a given value of the x-axis


## 1. fig. 2 :
as we can see, the packet length changes over time , in dependency of the way we've sent the messages in each interval. for example , in the text group graph, we can see that most of the messages were sent in batches or "bursts", since we did a lot of forwarding batches (the attacked user sends a group of messages that were sent in other whatssapp groups), and the length of most of the packets is smaller than 500. As opposed to the text group graph ,in the pics and video groups graphs, the length of most of the packets is between 2500 and 3000.

In the pics graph, we can see that most of the messages were sent in groups or "bursts" , similar to the text graph, but in the video graph , most of the messages were sent seperately , i.e, one video at a time (since the bars are thinner in the video graph).

examples of graphes - fig. 2:

<img src="resources/readme_pictures/without_noise/IMD_text_only.png"  width="40%">

<img src="resources/readme_pictures/without_noise/pics_only.jpeg"  width="40%">


## 2. fig. 3:
in the pdf graphs, the main reason for the distribution we've got is the way we've sent the messages. for example, in the pics and text groups, we've sent a lot of the messages together (in the text group- by forwarding , and in the pics- as a group of pictures), so the probability of big imds in those groups is smaller than the probability of big imds in the video group , since in this group, we've sent most of the videos seperately and not as a batch, so that the probability of having packets thart their IMD is bigger than 0 is bigger. this is why the PDF distribution is different in the video graph (there are peaks after x=0 too).

examples of graphes - fig. 3:

<img src="text_only_fig3.jpeg"  width="40%">

<img src="pics_only_fig3.jpeg"  width="40%">


## 3. fig. 4:
ccdf explanation: according to the definition of CCDF, the curve depicts the probability that an IM Size (normalized message size) of the group (this is the random variable x) is bigger than a given value of the x-axis.

we can see that for all the groups, when x=0, the probability that the message size is bigger than x is 1, since all of the messages wev've sent (normalized) have a size bigger than 0. and as x grows, we can see that each curve grows smaller (each one with respect to the frequency of the message sizes for the group), since these values are similar to the values of the normalized message sizes. and when x=1, the probability that the message size is bigger than x is zero , since all of the messages wev've sent (normalized) have a size smaller than the maximum size of message sizes (normalized).


<img src="ccdf_no_noise.jpeg"  width="40%">


## with noise 

***note - in this part, we've only recorded 2 types of groups - texts and pictures, since we've seen in the previous part (without noise), that the traffic on the text and audio groups and on the pictures and video groups is pretty simillar , in both packet lengths ranges and shape.

as we've mentioned before, the meaning of noise is capturing packets of whatsapp in wireshark, while using Spotify in the background.

fig. 2 - noise , no filtered: 

<img src="textonly_noise.jpeg"  width="40%">

fig. 3 - noise , no filtered: 

<img src="pics_noise.jpeg"  width="40%">


as we can see from the fig. 2 (packet length) above, since we didn't apply any filtering on the traffic , all of the packets are seen as "bursts" , hence the ranges of IMD are really small and close to 0 (this is due to the fact the Spotify keeps sending packets non-stop ,as long as we keep using it in the background). therefore, in the fig. 3 (PDF graph), we can see that without the filtering , we got a lot of packets with a very small range of IMD values , which made the PDF graph have an equal probability for each IMD of the packets ,and it wasn't able to detect the IMD values since they are very simillar.

this is why we decided to filter the traffic : the filters we have applied in this part (as we've mentioned in the documentation) are : tls || tcp || udp || quic , since tls is the protocol of whatssapp and all the others are protocols of Spotify .

fig. 2 - noise , filtered: 

<img src="pictures_tcp_tls_fig2.jpeg"  width="40%">

fig. 3 - noise , filtered: 

<img src="pictures_tcp_tls_fig3.jpeg"  width="40%">




as we can see, in fig. 2 with the filtering , the packet lengths are smaller , as we have filtered some of the traffic (the packets with the protocols that aren't the whatssapp or spotify protocols), but almost all of the traffic is still seen as "bursts", but this time , as we can see in fig. 3 , the IMD range is wider , due to the fact that traffic was reduced.


# case 2

this is the case where the attacked user may be active in several IM groups simultaneously.
just like the first case, there are two stages for this case - one without noise and one with noise

## without noise

fig.2 - no noise

<img src="no_noise_fig2.jpeg"  width="40%">


fig. 3 - no noise

<img src="all_no_noise_fig3.jpeg"  width="40%">

as we can see here, the traffic when the attacked user is active in several IM groups simultaneously (with no noise) is simillar to the traffic of case 1 (no simultaneously) with no noise of the pics and video groups, in regards to the range of the packet length, since it combines the traffic of all the groups , so that the packets with the biggest length are the ones from the pics and video groups (of course that there is also the chance of a very long text message). In addition , the sending ratio is simillar to the graphs in case 1 with no noise,  since we've tried to make a comparison between these graphs that is independent of the sending rate (so that we will actully see the difference in the traffic in dependence to the groups the user uses).


## with noise


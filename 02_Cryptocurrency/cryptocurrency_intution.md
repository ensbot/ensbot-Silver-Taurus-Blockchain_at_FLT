## **Cryptocurrency**

A digital currency in which encryption techniques are used to regulate the generation of units of currency and verify the transfer 
of funds, operating independently of a central bank. One such currency is `Bitcoin`.


#### **What is Bitcoin?**
_In crypto world there are three main layers:_
- _Technology_ : Blockchain (Modue-1)    
- _Protocol (Coin)_ : Bitcoin, Ethereum, Neo, Waves, Ripple, etc. (Module-2 : current)
- _Token_ : Smart Contracts (Module-3)

Bitcoin is about taking the blockchain technology form theory to practice so that a network of people can transact with each other.
So, these people don't need to have any intermediate between them and they don't need to trust a third party as they can trust the
whole system which will be same for everybody. It is about creating the protovol of helping people transact and an inherent means
of transacing is exchange of values. Also there can be other uses of blockchain in any field which can be made on top these (Bitcoin)
protocols.

_The Bitcoin Ecosystem:_
- _Nodes_ (refers to the devices or participants which are not mining in the network but only want to transact)
- _Miners_
- _Large Mines_
- _Mining Pools_
    

#### **Bitcoin's Monetary Policy**
- **Halving**
    This principle states that, the number of bitcoins per block released into the system is halved once every four year. And 
    the important point is that this monetary policy of bitcoin is entirely under the control of the algorithm that is in the
    bitcoin system software. So, after a certain time the reqard will be close to 0 and hence the transaction fees are meant
    to replace block rewardsbut this dependes on the market.
- **Block Frequency**
    This is how often those blocks come in which got rewards. So, it really depends on the design of the system.
        
        
#### **Understanding Mining Difficulty**
- **What is the Current Target and how does that feel?**
    As we have previously selected the Target as four-leading-zeros which reduces the pool size by one-fourth. As we are in a
    hexadecimal system, so for every leading zero the pool size reduces by one-sixteenth.
        
    > Let's do some estimations (Probabilty):
    Total possible 64-digit hexadecimal numbers = 16*16*...16 = 16^64 = 10^77
    Total valid hashes (with 4 leading zeros) = 16*16*...16 = 16^(64-4) = 2 * 10^72
    Probability that a random picked hash is valid = 2 * 10^72 / 20^77 = 2 * 10^(-5) = 0.002%
        
- **How is "Mining Difficulty" calculated?**
    Difficulty is adjusted every 2016 blocks (2 weeks). This is done by changing the number of leading zeros.
        
    > Difficulty = current target / max target
        

#### **Mining Pools**
What Mining Pool does is that, it distributes some power from the large mines among the small systems which adds up in their
hashing power reulsting in a much better hashing power. But there will be no meaning if they all are mining for the same block.
So it is important that they ensure that they can parallelize or distributex  the work. The fees for the mining is then distributed
among them on the basis of hashing power they provided into the mining pool. 
The higher the power pool has the larger will be the number of system it can have and hence more will be the chances of solving
the cryptographic puzzle. But since it has more number of system then the prize fees will gonna divide among them on basis of
their hashing power making the tradeoff applicable.
So, we can contribute in solving the cryptographic puzzle by using a mining rig and the necessary software to connect the hash
power of our rig with any of the mining pool. 


#### **Nonce Range**
Since we know that Nonce is the only field in the block that the miner can change in order to get the hash under the target limit.
But there is limit to the value of Nonce can hold. Since, Nonce is 32-bit number (precisely, 32-bit unsigned integer) and hence
it can anywhere between 0 and approx. 4 billion.

 > Let's do some estimations:
 _Difficulty_
 Total possible 64-digit hexadecimal numbers = 16*16*...16 = 16^64 = 10^77
 Total valid hashes (with 18 leading zeros) = 16*16*...16 = 16^(64-18) = 2 * 10^55
 Probability that a random picked hash is valid = 2 * 10^55 / 20^77 = 2 * 10^(-22)
 _Nonce_
 Max Nonce = 2^32 = 4 * 10^9
 Assuming no collision, this means 4 * 10^9 different hashes.
 Probability that one of them will be valid = 4 * 10^9 * 2 * 10^(-22) = 8 * 10^(-13) = 10^(-12) = 0.0000000001%

_Conclusion: One Nonce range is not enough_

Now say, a modest miner does 100MH/s. So,
    > 4 billion / 100 Million = 40 seconds
And if we don't get the value we have nothing to do after 40 seconds.

Now here we are going to be introduced with the new field: `timestamp`
This is considered as the `Unix time` that is the time passed since 1st of January 1970.

What _Timestamp_ does for us is: With every second the value of the timestamp changes and hence the value of hash will change
drastically due to avalanche effect. Now, what happens is, we try over a range of Nonces for 1 second and then the timestamp updates
and then we reset the Nonces to check the already checked Nonces but for a different timestamp and since even we are not reaching
the last values of the Total Nonce range we still getting more tries for finding the golden Nonce at any particular time rather than
getting finished after 40 seconds and having no means to find the golden Nonce.

Now, here we can get the insight of how mining pool is very useful, as we can provide different ranges, from 0 to 1 billion, 1 to 2
billion, 2 to 3 billion and 3 to 4 billion to different systems for different timestamps hence providing very high hashing power.
So, for a larger mining pool (having a power of 22 million trillion hashes per sec) can traverse the full Nonce range at a particular
timestamp in just few milliseconds. So, what will it do for rest of the milliseconds until the timestamp updates.


#### **How Miners pick their Transactions**
Since we know that adding a new block in the blockchain requires some time. But we do tansactions all the time. So what happens is
that our transactions get stored in a `MEMPOOL` which is similar to a staging area. So, a miner or node has a MEMPOOL attached to
them and so the miner will need to include some of these transactions in the block and let's say a miner has a maximum of 4 to 5
transactions that they can include in their MEMPOOL (staging area). In real world environment the limits is 1MB in which approx.
2000 transactions can include, but for example we are taking 5 transactions. Each transaction has a transaction ID with more info.
and the fees field that the minor will get for mining that transaction. So generally, the miners will be going to choose the highest
fees transaction.
Now say the Miner has gone with the 4 billions hashes within a second also, then what that Miner can do is to change the configuration
of the block and then restart the Nonce range. So, that even with high hashing powers, the Miner can continuosly mine without wasting
any time. So what the Miner can do to change the block configuration is that to change the lowest fee transaction from the data field
with another transaction which will have a fee next to the removed transaction from the MEMPOOL and the reapeat the process again in
that same timestamp for the Nonce range (reseted). Once the 1 second gets completed at the timestamp updates then the changed 
transaction will get changed back it's value to the originally choosen value.
So, if the fees is too low that your transaction can get stucked up in the MEMPOOL and get revert back to you after sometime.


#### **CPUs vs GPUs vs ASICs**
 > CPU = Central Processing Unit -- Genral -- less than 10MH/s
 
 > GPU = Graphics Processing Unit -- Specialized -- less than 1GH/s
 
 > ASIC = Application-Specific Integrated Circuit -- Totally Specialized -- more than 1000GH/s
 
In a ASIC the calculations are done on a logical level but rather on physcial level and hence is totally specialized for solving the
SHA-256 cryptographic puzzle.

But ASIC is only used with the Protocols (Coin) which uses the SHA-256 cryptographic algorithm like - Bitcoin. We can change it's
configuration to make it usable for other types of Cryptocurrencies. But so far, there is no configuration or implementation similar
to ASIC for Ethereum as it is memory heavy. So GPUs are there for Ethereum.


#### **How do Mempools work?**
As we know there is Mempool attached to every participant (node or miner) in the network and as it is peer-2-peer distributed network
then when one node performs some transaction then that transaction gets on it's mempool which then in turn relayed over the network
to the negihbour nodes and the miners and then all those participants can verify and account for that transaction, that whether or not
that transaction is geniune and then they relayed down that information across the network and so at last every single participant in
the network will get that transaction in it's mempool. So there can be generally more than 9000 or 10000 transactions sitting in the
mempool out of which upto 2000 can be there in the block for the mining process depending on the size of the transaction.


#### **Orphaned Blocks**
In case of the problem when more than miner found the answer for the puzzle but cannot be realyed due to time gap. Then the one block
which will get a new block after it first will be accpeted and will stay with the  reward while the other miner will have to auto
refund the reward money as it's block is rejected (known as `orphaned block`). Since, the minor should wait for atleast 6 more blocks
to be attached after your mined block to ensure that, there will be no problem of `block rejection` due to information relay lag
problem or otherwise they can reach on a situation where the goods are sold and the transaction they got gets reverted. This problem
is known as `Double Spend Problem`. The Miner whose block is to be accepted is based on more than 50 percent majority basis.


#### **The 51% Attack**
It's a hypothetical attack but it could possibly happen and it is commonly feared and discussed. The 51% attack is not an individual
attack to tamper with a selected block on more than 50 percent blockchains on the network (that is a different concept).
What really is the `The 51% Attack` is about is, suppose there are a bunch of miners mining for their blockchain and then their comes
some other group of minors offering them with the help (with the evil intent). Then they get a copy of their chain and set up everything
and then closed their connection with the outside world. Now say after a certain time the original miner's group mined two new blocks
but the other miner's group mined four blocks because they are large in numbers and so on, they both goes on mining and at last the
other group is having the blocks way more than (say, having a gap of 10blocks) that of original miner's gorup and all of the sudden
the other miner's group open the connection and broadcast their new blockchain and their progress online and so what happens in the
full network is that we have two competing chains and since the other miner's group is larger than that of the original miner's chain
and hence the original miner's chain will be invalid and they will have to refund their money back and can face a big loss and their
is nothing illegal happening here. What another thing the other miner's group can do, if they are smart is that, since they know that
they are gonna mine at a much faster rate than the original miner's group and will gonna revert their work (or transactions), then
the other miner's groups can beforehand, go to the stage where each of the blocks are being added to the chain of original miner's
blockchain and can purchase the goods from their transactions as a node, so that at the end, when the original miner's blockchain
will gonna get reject and the node gets the profit which is infact a member of other miner's gorup and hence the other miner's group
will gonna have double profit while the original miner's group will gonna face double loss (termed as `Double Spend Problem`).  


#### **Deriving the current target**
Say for example we have bitcoin block. Indside of that we do not have directly have a `target` field but a `bits` field. So we gonna
get to derive that traget value. For that we convert that bits value into hexaadecimal format we will get a hex-bit-value. Then we
choose the first two digits of the hex-bit-value and convert it back into decimal number system and say for example we get a value 23.
Then, we assume the value in bytes, as 23 bytes = 23 * 8 bits = 23 * 2 * 4 bits = 23 * 2 * Hex Digits. So, we will consider the hash
of length 46 hex digits. In this 46 hex digits the starting digits will be the rest of the digits of hex-bit-value and the 0s. The
rest of the values that are left out of 64 hex digits (i.e., 18 hex digits) will be considered as our 0s from the start to the value
which makes our target value.
                        

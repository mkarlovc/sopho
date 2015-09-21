REQUEST:
[from Anton]
Dear Jan
I hope you are doing well. I wanted to ask if you can provide us with some details from the twitter dataset we have.
Specifically, we would need 100 of most retweeted messages, and the details of the first issuer of the message (how many follower the issuer has, the time), and also details of the retweeter that had the most followers (i.e. how many he had, when in the "chain of events" did it happen, etc.). As an example;
message M was retweeted 10000 times, issued on Jan 1st 2015, by a user with 24 followers, and the retweeter with the most followers was the 50 person to retweet it, and he had 3000 followers.
I hope that makes sense. Is it possible this info is provided quickly? And how long should we wait? Thank you.
Have a lovely weekend.
RESULT:
(1) id_of_tweet,
(2) num_of_retweets,
(3) num_of_followers_of_tweet_issuer,
(4) time_ms_of_tweet,
(5) time_str_of_tweet,
(6) num_of_followers_of_max_retweeter,
(7) position_in_chain_of_max_retweeter

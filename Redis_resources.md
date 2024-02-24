# Requirements:
 - Problem statement
 - Why it matters
 - Theory and technology base
 - How to solve them
 - Demo
 - Presentation slides

# References
https://aws.amazon.com/redis/

https://backendless.com/redis-what-it-is-what-it-does-and-why-you-should-care/#1670599762368-db4223a0-cc7a

https://www.linkedin.com/pulse/why-when-use-redis-hamed-moayeri

http://oldblog.antirez.com/post/take-advantage-of-redis-adding-it-to-your-stack.html

https://redis.io/docs/about/

# Problem statement

## Slow latest items listings in your home page
Can I have a penny for every instance of the following query that is running too slow please?
SELECT * FROM foo WHERE ... ORDER BY time DESC LIMIT 10
To have listings like "latest items added by our users" or "latest something else" in web applications is very common, and often a scalability problem. It is pretty counter intuitive that you need to sort stuff if you just want to list items in the same order they were created.

## Leaderboards and related problems
Another very common need that is hard to model with good performances in DBs that are not in-memory is to take a list of items, sorted by a score, updated in real time, with many updates arriving every second.

The classical example is the leaderboard in an online game, for instance a Facebook game, but this pattern can be applied to a number of different scenarios. In the online game example you receive a very high number of score updates by different users. WIth this scores you usually want to:
Show a leaderboard with the top #100 scores.
Show the user its current global rank.

[Leaderboard System Design](https://systemdesign.one/leaderboard-system-design/)

## Order by user votes and time
A notable variation of the above leaderboard pattern is the implementation of a site like Reddit or Hacker News, where news are ordered accordingly to a forumla similar to:
score = points / time^alpha
So user votes will raise the news in a proportional way, but time will take the news down exponentially. Well the actual algorithm is up to you, this will not change our pattern.

This pattern works in this way, starting from the observation that probably only the latest, for instance, 1000 news are good candidates to stay in the home page, so we can ignore all the others. The implementation is simple:
Every time a new news is posted we add the ID into a list, with LPUSH + LTRIM in order to take only the latest 1000 items.
There is a worker that gets this list and continually computes the final score of every news in this set of 1000 news. The result is used to populate a sorted set with ZADD. Old news are removed from the sorted set in the mean time as a cleanup operation.

## Unique N items in a given amount of time
Another interesting example of statistic that is trivial to do using Redis but is very hard with other kind of databases is to see how many unique users visited a given resource in a given amount of time. For instance I want to know the number of unique registered users, or IP addresses, that accessed a given article in an online newspaper.

# Why it matters

- In-memory data store for ultra-fast data access and retrieval.
- Supports diverse data structures like strings, hashes, lists, sets, and more.
- Enables caching for frequent data reads and write optimization.
- Pub/Sub messaging for real-time data communication.
- High availability and scalability for mission-critical applications.


Example: News Website Powered by Redis
Problem: Imagine a rapidly growing news website with millions of daily visitors. Traditional databases struggle to handle the constant influx of requests, leading to slow page loading times and frustrated users.

Solution: Enter Redis!

In-memory data store: Redis stores frequently accessed data like news headlines, summaries, and user preferences in memory, offering lightning-fast retrieval compared to traditional databases.

Diverse data structures:

Hashmaps: Store detailed news articles with keys like article ID and values including title, author, content, etc.
Sorted sets: Order articles by popularity, trending topics, or specific categories for efficient retrieval.
Lists: Maintain queues for upcoming articles, live updates, or personalized content recommendations.
Sets: Track unique user visits, interests, or subscribed categories for targeted advertising and content suggestions.
Caching: Popular articles or user-specific data are cached, reducing database load and significantly improving response times, especially for repeated visitors.

Pub/Sub messaging: Real-time news updates are broadcasted via Pub/Sub, enabling instant notifications on user devices or live feed updates on the website.

High availability and scalability: Redis can be easily scaled horizontally by adding more nodes, ensuring smooth operation even during peak traffic periods. This guarantees high availability and prevents website downtime.

Benefits:

Faster loading times: Users get immediate access to news and updates, improving user experience and satisfaction.
Personalized content: Tailored recommendations based on user preferences and interests.
Real-time updates: Users stay informed with instant notifications on breaking news or relevant topics.
Scalability for growth: The website can handle increasing traffic without performance degradation.

# Theory and technology base

## Pub/Sub
Do you know that Redis includes a fairly high performance implementation of Pub/Sub?

Redis Pub/Sub is very very simple to use, stable, and fast, with support for pattern matching, ability to subscribe/unsubscribe to channels on the run, and so forth. You can read more about it in the Redis PubSub official documentation. https://redis.io/docs/interact/pubsub/

## Queues
You probably already noticed how Redis commands like list push and list pop make it suitable to implement queues, but you can do more than that: Redis has blocking variants of list pop commands that will block if a list is empty. https://redis.io/commands/blpop/

A common usage of Redis as a queue is the Resque library, implemented and popularized by Github's folks.

With our http://redis.io/commands/rpoplpush list rotation commands it is possible to implement queues with interesting semantics that will make your background workers happier! (For instance you can implement a rotating list to fetch RSS feeds again and again, so that every worker will pick the RSS that was fetched more in the past, and thus needs to be updated ASAP). Similarly using sorted sets it is possible to implement priority queues easily.

## Caching
This section alone would deserve a specific blog post... so in short here I'll say that Redis can be used as a replacement for memcached in order to turn your cache into something able to store data in an simpler to update way, so that there is no need to regenerate the data every time. See for reference the first pattern published in this article.

# How to solve them

https://systemdesign.one/leaderboard-system-design/small-scale-leaderboard-write-path.webp

A small-scale leaderboard can leverage the cache-aside pattern on the caching layer for the relational database. The following operations are performed when a player updates the score9:

- The client creates a WebSocket connection to the load balancer for real-time communication
- The load balancer delegates the client’s request to the closest data center
- The server updates the player’s score record on the relational database following the cache-aside pattern
- The server updates the same player’s score record on the cache server following the cache-aside pattern

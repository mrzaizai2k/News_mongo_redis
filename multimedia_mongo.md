Focus on “Data Engineering” point of view
 ◼ Available technologies may be employed to
solve the problem but with knowhow
 ◼ 20 minute presentation + 10 minute Q&A
 ◼ Every member must present
 ◼ Contribution of each member must be clearly
claimed
 ◼ An assigned review team will give feedback
and questions

◼ Problem statement and why it matters (1 point)
 ◼ Challenges in terms of data engineering (1.5
points)
 ◼ Theory and technology base (1 point)
 ◼ How to solve them (3 points)
 ◼ Demo (1.5 points)
 ◼ Report (2 points

https://www.youtube.com/watch?v=PT_yD9kG3M0

https://www.mongodb.com/developer/products/mongodb/storing-large-objects-and-files/

https://www.mongodb.com/developer/products/atlas/media-management-integrating-nodejs-azure-blob-storage-mongodb/

https://medium.com/@malcolm.wiredu/creating-an-amazon-s3-bucket-for-storing-media-and-static-files-for-your-website-dd8e348306ef

https://medium.com/@sidharthpurohit/system-designing-basics-designing-a-distributed-storage-service-in-cloud-a91ed91dfb22

## Theory/tech base, (s3)

Theory and Overview:

- AWS S3 is a highly scalable, secure, durable, and cost-effective object storage service provided by Amazon Web Services (AWS).
It allows users to store and retrieve any amount of data from anywhere on the web, offering a simple web service interface to store and retrieve data.

- S3 is designed to provide 99.999999999% (11 nines) durability of objects over a given year and 99.99% availability of the service.
Objects stored in S3 are organized into buckets, which are similar to folders or directories. Each bucket must have a unique name across the entire AWS S3 namespace.

- S3 supports a virtually unlimited number of objects and can store objects ranging in size from a few bytes to terabytes.

Technical Base:

- Storage Classes: AWS S3 offers various storage classes optimized for different access patterns and cost considerations, such as Standard, Intelligent-Tiering, Glacier, Glacier Deep Archive, etc. Each class has its own pricing model and characteristics.
Security: S3 provides robust security features to control access to data at various levels. This includes bucket policies, Access Control Lists (ACLs), Identity and Access Management (IAM) policies, encryption options (Server-Side Encryption, Client-Side Encryption), and AWS CloudTrail for auditing.

- Data Transfer: S3 supports both uploading and downloading of data over HTTP and HTTPS. It also offers features like Transfer Acceleration for faster uploads and downloads, and AWS Direct Connect for dedicated network connections.
Lifecycle Policies: S3 allows you to define lifecycle policies to automatically transition objects between different storage classes or delete them after a specified period. This helps in optimizing costs and managing data retention.

- Versioning: S3 supports versioning, which enables you to keep multiple versions of an object in the same bucket. This provides an additional layer of protection against accidental deletion or overwrites.

- Cross-Region Replication (CRR): This feature allows you to replicate data between different AWS regions asynchronously. It helps in disaster recovery, compliance, and low-latency access to data from different geographical locations.
Event Notifications: S3 can trigger events (e.g., object creation, deletion) and send notifications to AWS Lambda, SQS, or SNS, enabling you to automate workflows based on changes in your data.

https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html#ConsistencyModel

Amazon S3 provides strong read-after-write consistency for PUT and DELETE requests of objects in your Amazon S3 bucket in all AWS Regions. This behavior applies to both writes to new objects as well as PUT requests that overwrite existing objects and DELETE requests. In addition, read operations on Amazon S3 Select, Amazon S3 access controls lists (ACLs), Amazon S3 Object Tags, and object metadata (for example, the HEAD object) are strongly consistent.

Updates to a single key are atomic. For example, if you make a PUT request to an existing key from one thread and perform a GET request on the same key from a second thread concurrently, you will get either the old data or the new data, but never partial or corrupt data.

Amazon S3 achieves high availability by replicating data across multiple servers within AWS data centers. If a PUT request is successful, your data is safely stored. Any read (GET or LIST request) that is initiated following the receipt of a successful PUT response will return the data written by the PUT request. Here are examples of this behavior:

A process writes a new object to Amazon S3 and immediately lists keys within its bucket. The new object appears in the list.

A process replaces an existing object and immediately tries to read it. Amazon S3 returns the new data.

A process deletes an existing object and immediately tries to read it. Amazon S3 does not return any data because the object has been deleted.

A process deletes an existing object and immediately lists keys within its bucket. The object does not appear in the listing.

Note
Amazon S3 does not support object locking for concurrent writers. If two PUT requests are simultaneously made to the same key, the request with the latest timestamp wins. If this is an issue, you must build an object-locking mechanism into your application.

Updates are key-based. There is no way to make atomic updates across keys. For example, you cannot make the update of one key dependent on the update of another key unless you design this functionality into your application.

Bucket configurations have an eventual consistency model. Specifically, this means that:

If you delete a bucket and immediately list all buckets, the deleted bucket might still appear in the list.

If you enable versioning on a bucket for the first time, it might take a short amount of time for the change to be fully propagated. We recommend that you wait for 15 minutes after enabling versioning before issuing write operations (PUT or DELETE requests) on objects in the bucket.

Concurrent applications
This section provides examples of behavior to be expected from Amazon S3 when multiple clients are writing to the same items.

In this example, both W1 (write 1) and W2 (write 2) finish before the start of R1 (read 1) and R2 (read 2). Because S3 is strongly consistent, R1 and R2 both return color = ruby.


In the next example, W2 does not finish before the start of R1. Therefore, R1 might return color = ruby or color = garnet. However, because W1 and W2 finish before the start of R2, R2 returns color = garnet.


In the last example, W2 begins before W1 has received an acknowledgment. Therefore, these writes are considered concurrent. Amazon S3 internally uses last-writer-wins semantics to determine which write takes precedence. However, the order in which Amazon S3 receives the requests and the order in which applications receive acknowledgments cannot be predicted because of various factors, such as network latency. For example, W2 might be initiated by an Amazon EC2 instance in the same Region, while W1 might be initiated by a host that is farther away. The best way to determine the final value is to perform a read after both writes have been acknowledged.

1. Buckets

A bucket in Amazon S3 serves as a container for storing objects. Each bucket can hold an unlimited number of objects and is uniquely identified by a name. When creating a bucket, users must specify a name and choose the AWS Region where it will reside. Once created, the bucket name and Region cannot be changed. Key features of buckets include:

Namespace Organization: Buckets organize the S3 namespace at the highest level, providing a structured approach to data storage.
Cost and Access Control: Buckets identify the AWS account responsible for storage and data transfer charges and offer access control options such as bucket policies, ACLs, and S3 Access Points.
Usage Reporting: Buckets serve as the unit of aggregation for usage reporting, allowing users to monitor and analyze storage consumption.
For more detailed information on buckets, users can refer to the "Buckets overview" documentation.

2. Objects

Objects are the fundamental entities stored within Amazon S3. Each object consists of data and metadata, with metadata comprising name-value pairs describing the object's properties. Objects are uniquely identified within a bucket by a key (name) and, optionally, a version ID if S3 Versioning is enabled. Key features of objects include:

Unique Identification: An object is uniquely identified within a bucket by its key, allowing for efficient retrieval and management.
Metadata: Objects include metadata providing valuable information such as the date last modified and Content-Type.
Addressing: Objects can be addressed using a combination of the web service endpoint, bucket name, key, and optionally, a version, facilitating easy access and retrieval.
For more detailed information on objects, users can refer to the "Amazon S3 objects overview" documentation.

3. S3 Versioning

S3 Versioning is a feature that enables users to keep multiple variants of an object within the same bucket. With versioning enabled, every modification to an object results in a new version being created, allowing users to preserve, retrieve, and restore previous versions as needed. Key features of S3 Versioning include:

Data Preservation: Versioning preserves every version of every object stored in a bucket, providing protection against unintended user actions and application failures.
Unique Version ID: Each object added to a versioned bucket is assigned a unique version ID by Amazon S3, allowing for precise identification and retrieval.

![image](https://github.com/mrzaizai2k/News_mongo_redis/assets/40959407/fa654bc2-c42d-4727-b791-28d2e1f6c5df)


## How to solve them (s3)

## Compare S3 vs mongo

## Compare mongo vs SQL db

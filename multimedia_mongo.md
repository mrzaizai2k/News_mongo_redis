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

- Distributed Architecture: S3 is built on a distributed architecture, where data is stored across multiple servers and storage devices in AWS data centers around the world. This distributed approach enables horizontal scalability, allowing S3 to accommodate virtually unlimited amounts of data while ensuring high performance and fault tolerance.

- Object Storage: S3 employs an object storage model, where data is stored as objects rather than traditional file systems. Each object consists of data (the actual multimedia content) and metadata (information about the object, such as its size, content type, and storage class). This object-based approach offers greater flexibility and scalability compared to file-based storage systems.

- Redundancy and Durability: S3 is designed for durability, with data replicated across multiple storage devices within each AWS Availability Zone (AZ) and automatically backed up to other AZs within the same AWS Region. This redundancy ensures that data remains highly available even in the event of hardware failures or other disruptions.

- Storage Classes: S3 offers different storage classes optimized for various use cases and access patterns. These include Standard, Standard-IA (Infrequent Access), One Zone-IA, Glacier, and Glacier Deep Archive. Each storage class is designed to balance cost, performance, and durability based on the specific requirements of the data being stored.

- Multi-Tier Architecture: S3 employs a multi-tier architecture, where data is distributed across multiple tiers of storage based on access frequency and cost considerations. Frequently accessed data is stored in high-performance storage tiers, while infrequently accessed or archival data is moved to lower-cost storage tiers, such as Glacier or Glacier Deep Archive.

- Data Replication and Availability Zones: S3 replicates data across multiple Availability Zones within the same AWS Region to ensure high availability and fault tolerance. Availability Zones are physically separate data centers with independent power, cooling, and networking infrastructure, providing redundancy and resilience against localized failures.

- Scalability and Elasticity: S3 is designed to scale seamlessly with growing storage demands, automatically provisioning additional storage capacity as needed. This elasticity enables users to store and access virtually unlimited amounts of data without worrying about capacity constraints or performance degradation.

- Security Features: S3 offers robust security features to protect data at rest and in transit. These include server-side encryption (SSE), client-side encryption, access control mechanisms (IAM policies, bucket policies, ACLs), and integration with AWS Identity and Access Management (IAM) for fine-grained access control and authentication.

- APIs and Integration: S3 provides a simple and intuitive RESTful API for interacting with storage objects programmatically. This API allows developers to integrate S3 storage capabilities into their applications, enabling seamless data storage, retrieval, and management in the cloud.

## Compare S3 vs mongo
### High Performance

MongoDB	Amazon S3
The NoSQL nature of MongoDB makes data operations quick and easy. Without compromising the data integrity, data can be quickly stored, updated and retrieved.	AWS S3 provides actions such as multi-Part payload which gives low latency of 100–200 milliseconds which automatically grows to high request rates.

Resources
GridFS, a specification for storing and retrieving large files such as images, video files, and audio files with MongoDB, can impact performance based on the memory and processor capabilities of the hosting server. For smaller files accessed infrequently, GridFS might exhibit slightly superior performance to AWS S3 due to its streamlined operation within the database itself. However, for larger files or higher frequency access, S3's dedicated infrastructure might provide better performance due to its optimized data retrieval paths and global distribution networks.

Latency
The location of the storage platform relative to the application hosting environment plays a critical role in determining the actual performance experienced by end-users:

Amazon Hosted Applications: For applications running on the Amazon ecosystem, S3 offers lower latency due to optimized paths within the Amazon network, making it a superior choice for such setups.

On-Premises Applications: When the application is hosted on-premises, the choice between MongoDB and S3 becomes more nuanced. A MongoDB instance on the same network as the application would likely outperform S3 and even MinIO (a high-performance, AWS S3-compatible storage system) due to the absence of significant network latency.

Internet-Transferred Data: For applications where data must be transferred over the internet to a managed MongoDB instance or to S3, the network quality and distance can significantly impact performance. In such cases, S3's global infrastructure potentially offers more consistent and faster data access, particularly for applications already hosted within the Amazon ecosystem.

Processor and Memory Costs
MongoDB's architecture demands more in terms of memory and processing power compared to AWS S3. This is particularly relevant when dealing with the storage of large files at a high frequency. AWS S3, designed as an object storage service, is optimized for such tasks and thus incurs lower costs related to processing and memory usage. Therefore, for high-volume storage needs, S3 emerges as a more cost-effective choice.

Disk Space
The cost of disk space is another critical factor. If the primary concern is the storage of large files without a pressing need for speed, the decision boils down to the comparative costs of disk space. This requires a personalized calculation, considering the specific costs of disk space for your MongoDB setup versus the pricing tiers of AWS S3. For those who can manage with slower access speeds, the choice may hinge on which option offers the more economical storage per gigabyte.

Data Transfer Costs
Data transfer costs can significantly impact the overall cost, especially when storing and accessing large files. Amazon's pricing structure for bandwidth typically represents a higher cost compared to most self-hosted solutions or cloud servers from other providers. This aspect of cost becomes increasingly important with the volume of data transfer involved in large file storage and access. Consequently, for operations where large data transfers are common, a self-hosted MongoDB solution or an alternative cloud provider might offer cost advantages over AWS S3, depending on the specific bandwidth pricing models.

### Compare data type
BSON

BSON, which stands for Binary JSON (JavaScript Object Notation), is a binary-encoded serialization of JSON-like documents. It is designed to be efficient in space and speed when encoding and decoding data in MongoDB, a popular NoSQL database. BSON extends the JSON model to provide additional data types and to be efficient for encoding and decoding within different languages. 
Efficient Storage and Retrieval: BSON is designed to be more efficient than JSON in terms of storage space and scan-speed. It allows MongoDB to store types not represented in JSON, such as Date and binary data.

Object Files (in Amazon S3 Context)
In the context of Amazon S3, an object file refers to any piece of data stored in S3. An S3 object can be any file type - from simple text files and images to complex applications - stored in a flat, scalable storage structure. Unlike BSON, which is a specific data format, S3 objects are essentially binary files without any imposed structure, identified and accessed through keys (file names) within buckets (storage containers). 
Binary Data Format: S3 objects store data in a raw binary format. This means that S3 can store files in their native formats, be it images, videos, application data, or any other file type, without needing a specific data structure or format

### Data storage

- MongoDB Storage Characteristics:
Data Model: MongoDB is a document-oriented database that stores data in JSON-like (BSON) documents, allowing for a flexible and dynamic schema. This flexibility is advantageous for storing text and complex hierarchical data, which can change over time.
Storage Organization: Data in MongoDB is organized into collections and databases. Collections can be thought of as equivalent to tables in a relational database, but without a fixed schema. This organization suits applications that require rapid iteration and where data structures can evolve.
Suitability for Data Types:
Text: MongoDB's document model is inherently suited for storing and querying text documents, including JSON, XML, or BSON data, making it a good choice for content management systems, blogging platforms, or any application that handles a lot of variable text data.
Images and Videos: While MongoDB can store binary data (such as images and videos) using GridFS (when files exceed the BSON-document size limit of 16MB), it's generally not as efficient or cost-effective as using a dedicated object storage service like S3 for large or numerous multimedia files.

- Amazon S3 Storage Characteristics:
Data Model: S3 is an object storage service that treats data as objects. Each object is stored in a bucket and is identified by a unique key. Objects can contain data in any format (binary), making S3 extremely versatile for storing a wide variety of file types.
Storage Organization: S3 organizes data into buckets, which are similar to top-level directories. Within each bucket, objects can be further organized with keys that simulate a hierarchical structure (e.g., folder1/subfolder1/file1). Additionally, S3 data is stored across multiple facilities within a region, ensuring high durability and availability.
Suitability for Data Types:
Text: S3 can efficiently store large quantities of text data, such as logs or raw text files. However, for applications that require complex queries or frequent updates to text data, the flexibility of MongoDB might be more appropriate.
Images and Videos: S3 is particularly well-suited for storing and serving large files such as images and videos. Its high durability, availability, and built-in features like versioning and lifecycle management make it an ideal choice for media hosting, content delivery networks, and data archiving.

### Data Preprocessing

- In s3
A file is split into smaller blocks.
Each block is compressed using compression algorithms.
To ensure security, each block is encrypted before it is sent to cloud storage.
Blocks are uploaded to the cloud storage.

- In GridFs
  https://www.geopits.com/blog/mongodb-gridfs.html

  Instead of storing a file in a single document, GridFS divides the file into parts, or chunks [1], and stores each chunk as a separate document. By default, GridFS uses a default chunk size of 255 kB; that is, GridFS divides a file into chunks of 255 kB with the exception of the last chunk. The last chunk is only as large as necessary. Similarly, files that are no larger than the chunk size only have a final chunk, using only as much space as needed plus some additional metadata.

GridFS uses two collections to store files. One collection stores the file chunks, and the other stores file metadata. The section 
GridFS Collections
 describes each collection in detail.

When you query GridFS for a file, the driver will reassemble the chunks as needed. You can perform range queries on files stored through GridFS. You can also access information from arbitrary sections of files, such as to "skip" to the middle of a video or audio file.

![image](https://github.com/mrzaizai2k/News_mongo_redis/assets/40959407/b5a65e54-ed13-4e4a-b2e2-9a17882a28de)

### Scaling 

MongoDB	Amazon S3
As the data grows, MongoDB quickly and equally distributed the data across a cluster of computers. This process is called "Sharding". Growing amounts of data are easily handled with MongoDB's scalability.	There is no set limit on the volume of data or the number of objects that can be stored in an S3 bucket. S3 offers infinite scalability. A bucket created in s3 has a 5T storage limit

Horizontal Scaling
Horizontal scaling, involving the expansion of storage space and processing nodes, presents different challenges and cost considerations for MongoDB and Amazon S3:

MongoDB: Horizontal scaling with MongoDB necessitates increased processor and memory resources as additional nodes are added to the cluster. This scaling approach can lead to escalating costs, particularly as the infrastructure grows. Consequently, the cost-effectiveness of MongoDB diminishes with the expansion of nodes. However, for local deployments, solutions like MinIO may offer a more cost-effective horizontal scaling option compared to MongoDB, leveraging cheaper local resources.

Amazon S3: Scalability with Amazon S3 is generally more cost-effective due to its native support for horizontal scaling and auto-scaling capabilities. S3's infrastructure allows for seamless expansion of storage space and processing capacity as demand grows. While MinIO hosted locally may provide a cheaper horizontal scaling alternative, it lacks the auto-scaling features and global infrastructure of Amazon S3, which could be crucial for applications with high availability and performance requirements.

Vertical Scaling
Vertical scaling, involving increasing the capacity of individual nodes, also presents distinct cost implications for MongoDB and Amazon S3:

MongoDB: As the pressure on the storage system increases, the cost of vertical scaling with MongoDB may become more significant. MongoDB requires additional processor and memory resources to handle higher loads efficiently. This approach can lead to higher costs as the infrastructure needs to be continuously upgraded to meet growing demands.

Amazon S3: Vertical scaling considerations with Amazon S3 are less pronounced compared to MongoDB. S3's architecture abstracts away the underlying infrastructure, allowing for seamless expansion of storage capacity without the need for manual adjustments to individual nodes. However, as with any cloud service, costs may still increase linearly with storage usage, but without the need for upfront investment in hardware upgrades
## Compare mongo vs SQL db

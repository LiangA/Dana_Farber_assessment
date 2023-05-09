# Dana_Farber_assessment
This file will serve as the navigator for the entire assessment. You can view the results of each implementation through the links provided.

Before starting, please clone the entire repository to your local machine:
```
cd ~
git clone https://github.com/LiangA/Dana_Farber_assessment.git
cd  Dana_Farber_assessment
```
Put the corresponding test data into this folder, and you can start playing with the project.

## BioInformatics & Data Handling
I used Python 3.11.2 for development, but you should be able to run it smoothly with any version of Python 3.9 or above. This assessment requires "requests" library be installed. Just run
```python 
pip install -r requirements.txt
```
in the project directory, and the installation should be done.

For most tasks except the Ensembl API one, the same report.py file is used for processing, and each task has a corresponding mode and required parameters. Please refer to the following instructions or enter the following command:
```python 
python report.py --help
```
and read the document.

### Task 1-1
> Recursively find all FASTQ files in a directory and report each file name and the percent of sequences in that file that are greater than 30 nucleotides long.
The input is a directory contains at least one fastq file in it.

You must use the following command to perform the test:
```python
python report.py --mode fastq --fq <directory>
```
You will see output similar to the following:
```
alden@DESKTOP-PTP549K:~/dana_farber_assessment$ python report.py --mode fastq --fq ./sample_files/
2023-05-04 01:55:05 root INFO starting function assign_files ...
2023-05-04 01:55:05 root INFO starting function check_assigned_file_format ...
2023-05-04 01:55:05 root INFO starting function divide_files ...
2023-05-04 01:55:05 root INFO starting function map ...
2023-05-04 01:55:05 root INFO starting function reduce ...
2023-05-04 01:55:05 root INFO starting function build ...

The percent of sequences are greater than 30 nucleotides long for each file:
Sample_R1.fastq: 80.6424%
Sample_R2.fastq: 83.6010%
```
> Note: --fq can also be replaced with --fastq-directory

### Task 1-2
> Given a FASTA file with DNA sequences, find 10 most frequent sequences and return the sequence and their counts in the file.
The input is a directory(file path) of a fasta file.

You must use the following command to perform the test:
```python
python report.py --mode fasta --fa <directory>
```
You will see output similar to the following:
```
alden@DESKTOP-PTP549K:~/dana_farber_assessment$ python report.py --mode fasta --fa ./sample_files/fasta/sample.fasta 
2023-05-04 02:00:04 root INFO starting function assign_files ...
2023-05-04 02:00:04 root INFO starting function check_assigned_file_format ...
2023-05-04 02:00:04 root INFO starting function divide_files ...
2023-05-04 02:00:04 root INFO starting function map ...
2023-05-04 02:00:04 root INFO starting function reduce ...
2023-05-04 02:00:04 root INFO starting function build ...

10 most frequent sequences and their counts in the file:
CGCGCAGGCTGAAGTAGTTACGCCCCTGTAAAGGAATCTATGGACAATGGAACGAACA: 28
TGTTCTGAGTCAAATGATATTAACTATGCTTATCACATATTATAAAAGACCGTGGACATTCATCTTTAGTGTGTCTCCCTCTTCCTACT: 27
CTCAATCTGCCAAGACCATAGATCCTCTCTTACTGTCAGCTCATCCGGTGAGGCC: 22
CCTGTTGCTGACTCAAGACATTAGTGAGAAATAAGACTTCTGCGATGCTCACCACTGCAATTGCTCATGCAAAATTGCGTTTAACAGG: 21
TTTCAGCTGTCTTTTAAGCAGAAGCGATTTGTCCAACAAAAACAACGCTGTTTACGAA: 17
ATTGCGAATTCCGCCTGTGTCCCCCACACGAGCGTGAATCGTGGCTAGAAGTTCAGCCCCTCTTAGCACAGAGTGAG: 17
TCACGCAGACAACGAACTGTGTCTGGATCAAAGACATCCGATAAGGCGATTCGTCTAGAAGGGTTACACAGTTGGGACCGGTAG: 8
GACACAAACACCGTGGCTCAACCTAATCCTATTAGAGCCGAAAAGGCGAGGATGCTGATTGAGTAGGTATCTGGA: 8
TGTGCAGAATATAATGTAAAAAAAACAGGACCCGGCTCTGTGCCGTTGGCCTGCGCGGTACTCATGTTAGTTTTCCGACTCCGACTTAT: 5
TGCTTAAACTCATGATAGTCCCTGAGTAAACTGGTTGCGACACGGCTCCCG: 5
```
> Note: --fa can also be replaced with --fasta-directory

### Task 1-3
> Given a chromosome and coordinates, write a program for looking up its annotation. Keep in mind you'll be doing this annotation millions of times. Output annotated file of gene name that input position overlaps.
The input will be two file paths: coordinates_to_annotate.txt and hg19_annotations.gtf respectively.

You must use the following command to perform the test:
```python
python report.py --mode annotation --ctoa <coordinates to annotate file path> --hg19 <hg19 annotations file path>
```
You will see output similar to the following:
```
alden@DESKTOP-PTP549K:~/dana_farber_assessment$ python report.py --mode annotation --ctoa ./sample_files/annotate/coordinates_to_annotate.txt --hg19 ./sample_files/gtf/hg19_annotations.gtf
2023-05-04 02:01:56 root INFO starting function assign_files ...
2023-05-04 02:01:56 root INFO starting function divide_files ...
2023-05-04 02:02:22 root INFO starting function map ...
2023-05-04 02:03:35 root INFO starting function reduce ...
2023-05-04 02:03:35 root INFO starting function build ...

A file "annotated_file" is created, it shows distinct pairs of chromosome, coordinate and annotation.
```
You can open the annotated_file with any text editor, and you will see data like this:
```
...
chr12	6646318	not matched
chr12	20704391	not matched
chr12	20704415	PDE3A
chr12	20704362	PDE3A
chr12	20704387	not matched
chr12	20704366	not matched
chr12	20704370	PDE3A
chr12	20704375	not matched
chr12	20704399	not matched
chr12	127650875	not matched
chr12	127650878	not matched
chr12	20704377	not matched
chr12	20704424	PDE3A
...
```
> Note: --ctoa can also be replaced with --coordinates_to_annotate_directory
--hg19can also be replaced with --hg19_annotations_directory

### Task 2
> Parse the given Example.hs_intervals.txt file. The file contains information on covereage on exon level in a hybrid capture panel. The file is a tab-delimited text file. Report the mean target coverage for the intervals grouped by GC% bins. Bin in 10%GC intervals (e.g. >= 0 to < 10; >= 10 to < 20; etc). Note that in the file, GC values range from 0 to 1 rather than percentage.
The input will be file path of Example.hs_intervals.txt file.

You must use the following command to perform the test:
```python
python report.py --mode interval_mean --intvl ./Example.hs_intervals.txt <hs intervals file path>
```
You will see output similar to the following:
```
alden@DESKTOP-PTP549K:~/dana_farber_assessment$ python report.py --mode interval_mean --intvl ./Example.hs_intervals.txt
2023-05-04 02:11:52 root INFO starting function assign_files ...
2023-05-04 02:11:52 root INFO starting function divide_files ...
2023-05-04 02:11:52 root INFO starting function map ...
2023-05-04 02:11:52 root INFO starting function reduce ...
2023-05-04 02:11:52 root INFO starting function build ...

The mean target coverage for the intervals grouped by GC% bins:
GC% bin 00- 10%: 0.0000
GC% bin 10- 20%: 69.2911
GC% bin 20- 30%: 77.9344
GC% bin 30- 40%: 99.0058
GC% bin 40- 50%: 101.2831
GC% bin 50- 60%: 92.1238
GC% bin 60- 70%: 78.9251
GC% bin 70- 80%: 37.8332
GC% bin 80- 90%: 10.2835
GC% bin 90-100%: 0.0000
```
> Note: --intvl can also be replaced with --hs_intervals_directory

### Task 3
> Given a list of variant IDs, using Ensembl API retrieve information about alleles, locations, 
effects of variants in transcripts, and genes containing the transcripts.

You can use the following command to perform the test:
```python
python ensembl.py -v <the variant ids separated by space>
```
You will see output similar to the following:
```
variant id      transcript id   start   end     allele(s)       gene symbol     gene id consequence
rs56116432      ENST00000453660 133256042       133256042       C/T     ABO     ENSG00000175164 non_coding_transcript_exon_v
ariant
rs56116432      ENST00000538324 133256042       133256042       C/T     ABO     ENSG00000175164 missense_variant
rs56116432      ENST00000611156 133256042       133256042       C/T     ABO     ENSG00000175164 missense_variant
rs56116432      ENST00000647353 133256042       133256042       C/T     ABO     ENSG00000175164 intron_variant
rs56116432      ENST00000647353 133256042       133256042       C/T     ABO     ENSG00000175164 non_coding_transcript_variant
rs56116432      ENST00000651471 133256042       133256042       C/T     ABO     ENSG00000175164 downstream_gene_variant
rs56116432      ENST00000679909 133256042       133256042       C/T     ABO     ENSG00000175164 intron_variant
rs56116432      ENST00000680600 133256042       133256042       C/T     ABO     ENSG00000175164 upstream_gene_variant
rs56116432      ENST00000626615 133256189       133256189       C/T     ABO     ENSG00000281879 missense_variant
rs56116432      ENST00000644422 133256189       133256189       C/T     ABO     ENSG00000281879 missense_variant
rs56116432      ENST00000644755 133256189       133256189       C/T     ABO     ENSG00000281879 missense_variant
rs56116432      ENST00000645810 133256189       133256189       C/T     ABO     ENSG00000281879 missense_variant
COSM476         140753336       140753336       COSMIC_MUTATION
```
Or, you can try another way to input the variants:
```python
python ensembl.py -vdir <a path to a file contains variant ids separated by line>
```
The same output will be expected.

> Note: --v can be replaced with --variants and -vdir can be replaced with --variant-directory. Exactly one of them must be provided, less or more will cause an error.

## Cloud Computing
> 1. How would you architect a framework for sharing large files (10Gb-25Gb) on the cloud with access controls at the file level? We want to share the same file with multiple users without making a copy. The users should be able to have access to the data on any cloud platform to run bioinformatics analysis pipelines. The users can run any cloud service, there is no restriction. The framework’s responsibility is only to make data accessible with access controls.

![diagram](diagram.png) 
To provide a concise answer, I would utilize a cloud storage service like S3, implement Access Control Lists (ACLs) for file-level access control, and secure the files with API Gateway and DNS services. Here are the reasons for this approach:

1. Cloud storage services like AWS S3, Azure Blob Storage, or GCP Cloud Storage offer high accessibility with the ability to handle high concurrent reading. For example, S3 has no volume restrictions except for a 5TB limit on individual files.
2. There is no need to create additional copies of the files, but replicas can be created to increase reliability or improve reading speed at remote locations.
3. ACL services are powerful tools for managing file object access. When combined with IAM, bucket-level and object-level access management can be implemented.
4. Using Route 53 and API Gateway together provides access control and traffic routing capabilities, which are particularly useful for external users. Domain names can be used to make API calls, and Route 53's health check feature ensures that requests are routed to healthy API endpoints most of the time.

> 2. Evaluate the benefits and limitations of using containerization and container orchestration technologies, such as Docker and Kubernetes, for deploying and managing bioinformatics HPC workloads in the cloud.

Here are some of the benefits and limitations of using container orchestration technologies:

Benefits:

1. Independency: Container seperate runtime environments. That creates the isolation of applications and their dependencies, which can help ensure that different applications do not interfere with each other.
2. Portability: Containers are portable across different environments and platforms.
3. Scalability: Container orchestration tools like Kubernetes can help automate the horizontal scaling of workloads based on demand. It is more powerful and more efficient when using cloud services.
4. Better CI/CD: Containerization allows for consistent deployment of applications. More over, we can deploy across different environments, which can reduce errors and increase reliability.

Limitations:

1. Complexity: Containerization and container orchestration can add complexity to the deployment and management.
2. Performance: Running containers can come with a performance penalty, particularly when compared to running applications natively on the host system.
3. Security: Containers can introduce new security challenges, particularly if they are not configured correctly or if vulnerabilities are not patched.

Overall, I would say the pros is over cons, especially for teams that are experienced with these technologies. However, we still need to carefully consider their specific needs and the associated costs and complexity before deciding to adopt them.

## SQL
> 1. For the following SQL statement, what is wrong with it and how would you fix it:
```SQL
-- Question:
SELECT UserId, AVG(Total) AS AvgOrderTotal
FROM Invoices
HAVING COUNT(OrderId) >= 1
```

Regarding this issue, in the absence of objective statement of the query, I made the following assumption: I need to add something to the existing query to make it reasonable and executable.

With this premise, I believe that this query is missing two things:

1. GROUP BY: Because the aggregate function AVG is used, we must add the GROUP BY keyword. I think it makes sense to group by UserID by observing the original query.
2. SELECT OrderId: In the HAVING clause, there is a condition COUNT(OrderId) >= 1, but the OrderId is not selected in the SELECT clause. It should be added.

So, the correct SQL query should be:
```SQL
SELECT UserId, OrderId, AVG(Total) AS AvgOrderTotal
FROM Invoices
GROUP BY UserId
HAVING COUNT(OrderId) >= 1;
```

## Worth mentioning
In this section, I would like to make a note of some of the assumptions and design ideas that were incorporated into this project. 

### Implementation practices

1. Long naming

In this project, I rarely use common abbreviations for variable names such as using "Algo" instead of "Algorithm". Instead, I try to write out the full words as much as possible. For engineers, these common abbreviations can effectively save code length and even accelerate the development process.

However, I believe that for a novice programmer or a PM without a computer science background, reading code full of abbreviations is more painful. Considering their needs, I tend to write out the full word without causing the code to become too verbose. Moreover, with the help of an IDE, we do not need to type a lot more keyboard strokes to write out the full words. So why not help them a bit?

2. Less-or-no comments

I admit that I'm lazy to write comments. But there is an idea that I agree with and am trying to adapt: code tells you how, comments tell you why. In my previous positions, I had a bad experience that the code and the comment isn't compatible. Comment itself can be a failure point if it lacks of maintenance! And maintainence also costs time and energy. So less comments, less possible faults. It's not telling us not to write comments, but hoping that we write it when we must do it. 

And I put date in comments. In a rebased code, there is a chance that we will lose the information of who and when commits the code. Putting date can remind us if this comment is too old to trust.

### Design

1. Builder pattern    

Except for the Ensembl API task, I employ the Builder pattern in all coding tasks. In the base ReportBuilder class, I treat the output of each task as a report and define the steps (functions) as follows: assign_files, check_assigned_file_format, divide_files, map, reduce, and build. The step check_assigned_file_format is optional, as it is beneficial to format and clean the data before report generation. However, since the example input files are not thoroughly cleaned, including an optional step can be helpful. Furthermore, running the steps out of order will result in errors in the program.

2. Decorator pattern

The Decorator pattern is widely recognized as a powerful and popular design pattern in Python. To enhance its functionality and ease of use, I implemented a decorator called show_running_info which is capable of logging out the running message for each step. By applying this decorator to each step, I was able to avoid the hassle of manually maintaining multiple logging statements.

3. Generator pattern

To optimize the memory usage when dealing with large files, I have implemented a lazy file reader, which is essentially a file reading generator. It generates only the required lines of the file, without loading the entire file into memory at once. This approach is extremely beneficial in cases where the file size is very large and loading it all at once would consume a significant amount of memory resources. With this implementation, we can save a considerable amount of memory and process the file more efficiently.

4. Asynchronous 

In the context of the Builders, the map function is implemented as an asynchronous function. This design choice allows for the efficient generation of reports, especially in a distributed system where multiple nodes can work on different parts of the task simultaneously. By leveraging the power of cloud services, we can take full advantage of asynchronous implementation, which offers better performance compared to traditional multi-threading or multi-processing.

Unlike traditional multi-threading or multi-processing implementations, which are limited by the resources of a single machine, cloud-based asynchronous implementation can dynamically allocate computing resources to different nodes based on the task's needs. This feature makes it an ideal choice for High-Performance Computing (HPC) applications, where tasks require a significant amount of computing power. By combining asynchronous implementation with cloud services, we can improve the efficiency and scalability of our report generation process, making it suitable for large-scale data processing tasks.

In summary, the combination of asynchronous implementation and cloud services offers significant benefits in terms of efficiency and scalability, making it a powerful tool for HPC applications.
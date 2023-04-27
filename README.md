# Folder Synchronization

This script synchronizes two folders periodically: a source folder and a replica folder. The program maintains a full, identical copy of the source folder at the replica folder. Synchronization is one-way: after synchronization, the content of the replica folder matches exactly the content of the source folder.


## Usage

```python
python sync_folders.py source_path replica_path interval log_file_path

```
where:

* source_path is the path to the source folder.
* replica_path is the path to the replica folder.
* interval is the synchronization interval in seconds.
* log_file_path is the path to the log file.

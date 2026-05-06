1. Creating and Renaming Files/Directories
Create a directory named test_dir using mkdir.
Inside test_dir, create an empty file called example.txt.
Rename example.txt to renamed_example.txt using mv
Explanation:
mkdir creates a new directory.
touch creates an empty file.
mv renames or moves files.
After execution, test_dir contains renamed_example.txt.




2. Viewing File Contents
Use cat to display the contents of /etc/passwd.
Display only the first 5 lines of /etc/passwd using head.
Display only the last 5 lines of /etc/passwd using tail.

Explanation:
cat prints the entire file.
head -n 5 shows the first 5 lines.
tail -n 5 shows the last 5 lines.
Useful for quickly inspecting configuration or log files.
3.Searching for Patterns
Use grep to find all lines containing the word "root" in /etc/passwd.

Explanation: grep searches for text patterns. Here it finds all lines containing "root". Typically, this shows the root user entry.
4. Zipping and Unzipping
Compress the test_dir directory into a file named test_dir.zip using zip.
Unzip test_dir.zip into a new directory named unzipped_dir.


Explanation:
zip -r compresses the directory recursively.
unzip -d extracts into a new directory.
After extraction, unzipped_dir/test_dir contains the original files.


5. Downloading Files
Use wget to download a file from a URL (e.g., https://example.com/sample.txt).





	Explanation: wget downloads files from the internet. The file sample.txt will be saved in the current directory. You can rename or specify a directory with -O or -P.

6. Changing Permissions
Create a file named secure.txt and change its permissions to read-only for everyone using chmod.



Explanation:
chmod 444 sets read-only permissions for owner, group, and others.
ls -l verifies with -r--r--r--.
This ensures no one can modify the file.


7. Working with Environment Variables
Use export to set a new environment variable called MY_VAR with the value "Hello, Linux!".


Explanation:
export sets an environment variable.
echo $MY_VAR displays its value.
Environment variables are used to store configuration or runtime values.

Submission Guidelines -: Attach Screenshots or command along with explanation and submit in doc(google doc or microsoft doc) format also attach github repo link


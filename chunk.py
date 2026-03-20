import os

chunk_no= 0
chunk_size = 1024

def get_chunks_by_number(filename,chunk_no, chunk_size):

   try:
       with open(filename, 'rb') as f:     # return one chunk of data based on the chunk number and chunk size
        f.seek(chunk_no * chunk_size) 
        data = f.read(chunk_size)
        return data   
                  
   except FileNotFoundError:
       print("File not found.")
       exit()

def get_total_chunks(filename, chunk_size):  #find total number of chunks in the file size of file
    # Helps the protocol know when to stop
    size = os.path.getsize(filename)
    return (size + chunk_size - 1) // chunk_size
 

 

    


       
    
   
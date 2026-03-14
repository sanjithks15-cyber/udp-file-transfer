

chunk_no= 0
sender_buffer_size =3

def get_chunks(filename, chunk_size):

    chunk =[]

    try:
       file = open(filename, "rb")
    except FileNotFoundError:
       print("File not found.")
       exit()

    while True:

        
        data = file.read(chunk_size)

        

        if not data:
            break

        chunk.append(data)

    file .close()

    return chunk   

    


       
    
   
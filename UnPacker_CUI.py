import os

def unpacker():
    print("-----------------------------------------------------")
    print("------------- Packer Unpacker CUI Module ------------")
    print("-----------------------------------------------------")
    
    print("---------------- Unpacking Activity -----------------")
    print()
    
    PackedFile = input("Enter the name of Packed file that you want to open: ")
    
    if not os.path.isfile(PackedFile):
        print("Unable to proceed as Packed file is missing...")
        return
    
    try:
        with open(PackedFile, 'rb') as fiobj:
            iCount = 0
            
            while True:
                Header = fiobj.read(100)
                if not Header:
                    break
                
                HeaderX = Header.decode().strip()
                Tokens = HeaderX.split(" ")
                
                file_name = Tokens[0]
                print(f"File drop with name: {file_name}")
                
                FileSize = int(Tokens[1])
                Buffer = fiobj.read(FileSize)
                
                with open(file_name, 'wb') as foobj:
                    foobj.write(Buffer)
                
                iCount += 1
            
            print("-----------------------------------------------------")
            print("Unpacking activity completed..")
            print(f"Number of files unpacked: {iCount}")
            print("-----------------------------------------------------")
        
    except Exception as e:
        print(f"Error during unpacking: {e}")
    
    print("Thank you for using Packer Unpacker tool")

if __name__ == "__main__":
    unpacker()

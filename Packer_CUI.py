import os

def main():
    print("-----------------------------------------------------")
    print("------------- Packer Unpacker CUI Module ------------")
    print("-----------------------------------------------------")
    
    print("----------------- Packing Activity ------------------")
    print()
    
    FolderName = input("Enter the name of Directory that you want to open for packing: ")
    
    if not os.path.isdir(FolderName):
        print("Directory does not exist")
        return
    
    PackedFile = input("Enter the name of packed file that you want to create: ")
    
    try:
        with open(PackedFile, 'wb') as foobj:
            iCount = 0
            
            for root, dirs, files in os.walk(FolderName):
                for file in files:
                    if file.endswith(".txt"):
                        file_path = os.path.join(root, file)
                        print(f"File packed with name: {file}")
                        
                        header = f"{file} {os.path.getsize(file_path)}".ljust(100)
                        foobj.write(header.encode())
                        
                        with open(file_path, 'rb') as fiobj:
                            while chunk := fiobj.read(1024):
                                foobj.write(chunk)
                        
                        iCount += 1
            
            print("-----------------------------------------------------")
            print("Packing activity completed..")
            print(f"Number of files packed: {iCount}")
            print("-----------------------------------------------------")
    
    except Exception as e:
        print(f"Unable to create packed file: {e}")
    
    print("Thank you for using Packer Unpacker tool")

if __name__ == "__main__":
    main()

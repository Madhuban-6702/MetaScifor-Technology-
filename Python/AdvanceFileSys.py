#Advance File System
class AdvanceFileSystem:
  def create_file(self,file_name,content=""):
    file=open(file_name,"w")
    file.write(content)
    print(f"File '{file_name}' created!!")
  
  def read_file(self,file_name):
    file=open(file_name,"r")
    print(file.read())
  
  def append_to_file(self,file_name,content):
    file=open(file_name,"a")
    file.write(content)
    print(f"Content appended to '{file_name}'")
  
  def overwrite(self,file_name,content):
    file=open(file_name,"w+")
    file.write(content)
    print(f"File '{file_name}' overwritten")

def main():
  fs=AdvanceFileSystem

  print("------Advance File System------")
  while True:
    print("\nSelect an Operation")
    print("1. Create File \n2. Read File \n3. Append File \n4. Over Write File \n5. Exit")

    choice=input("Enter Your Choice: ")

    if choice == '1':
      file_name=input("Enter the file name: ")
      content=input("Enter content for the file: ")
      fs.create_file(file_name,content)
    
    elif choice == '2':
      file_name=input("Enter the file name to read: ")
      fs.read_file(file_name)
    
    elif choice == '3':
      file_name=input("Enter the file name to append: ")
      content=input("Enter content to append: ")
      fs.append_to_file(file_name,content)
    
    elif choice == '4':
      file_name=input("Enter the file name to overwrite: ")
      content=input("Enter new content to overwrite: ")
      fs.overwrite(file_name,content)
    
    elif choice == '5':
      print("Exiting....")
      break
    
    else:
      print("Invalid Choice!!!")


if __name__ == "__main__":
  main()
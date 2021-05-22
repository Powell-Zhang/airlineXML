# airlineXML
## Installation
to install, simply clone this github repo. This can be done manually, by clicking the green button with the download symbol that says code, or through the command line using the following command:
```console
$ git clone https://github.com/Powell-Zhang/trieCLI
```
The non-python files are just here for demonstration and are not necessary for actual usage. 
## Usage
This program allows people to parse airline xml data to get a json seatmap. To run the program, simply put the python file in the same directory as the file you want to parse and run this command, replacing \<fileName\> with the name of the file:
```console
$ python seatnapParse.py <fileName>
```
**Note:** this method will only work with the sample files and their given names. The sample files have vastly different formats, so I wrote separate programs to parse each of them. For a more general usage, you can use this command, replacing \<fileName\> and \<num\> with either 1, if the file is in the same format as the sample file seatmap1.xml, or 2, if the file is in the same format as the sample file seatmap2.xml.  
```console
$ python seatnapParse.py <fileName> <num>
```
## Result
This program will produce a file named \<fileName\>\_parsed.json. This contains the JSON data of the seatmap, divided up by row, with the following format.


```
{

  'Rows': [
  
    {
    
      'Seats': [
      
        {
          
          'Element Type': Seat/Kitchen/Bathroom etc
          'Seat Type': Window/Center/Aisle
          'ID': Seat number (i.e. 18A)
          'Price': Price as an int 
          'Class': Economy/First/Business
          'Availability': Boolean for if the seat is available
          'Misc': List of other miscelaneous characteristics
        
        }
        ...
      
      ]
    
    }
    ...
  
  ]

}
```
**Note:** For both sample files I couldn't find any seats that weren't actually seats but were instead bathrooms, so the 'Element Type' variable is rather useless. Also, seatmap2.xml did not contain any class or price information, so those values are all none in the result. 

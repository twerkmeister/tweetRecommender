import csv

#format attributes [(name,attribute)]
def csv_to_arff(csv_filename, arff_filename, attributes, relation = "nothing"):
    csv_file = open(csv_filename)
    csv_file_sniff = open(csv_filename)        
    with open(arff_filename, "w") as output:            
        if csv.Sniffer().has_header(csv_file_sniff.read(1000)):            
            next(csv_file, None)      
        output.write("@RELATION %s \n" % relation)
        for attribute in attributes:         
            output.write("@ATTRIBUTE %s %s\n" % (attribute[0], attribute[1]))                            
        output.write("@DATA\n")
        for row in csv_file:
            output.write(row)
        output.close()    
    csv_file.close()  
    csv_file_sniff.close()  

if __name__ == '__main__':    
    attributes = [("webpage","string"),("rating","real"),("tweet","string"), ("uid","string")
                  ,("lda","real"),("language_model","real"), ("text_overlap","real"), ("length", "integer")]
    csv_to_arff('../dump/twitter_subset/evaluationEnriched.csv', "result.arff", attributes)

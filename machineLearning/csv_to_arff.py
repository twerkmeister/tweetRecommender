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
    attributes = [("webpage","string"),("rating","{1,-1}"),("tweet","string"), ("uid","string")
                  ,("lda","real"),("language_model","real"), 
                  ("tweet_length","integer"),("chars","integer"),
                   ("isverified","{true,false}"),("followers_count","integer"), ("statuses_count","integer"),
                   ("listed_count","integer"),("friends_count","integer"),
                   ("absolute_time_difference","integer"),("relative_time_difference","integer"),
                   ("binary_decision","integer"),("capped_time_after","integer"),
                   ("contains_url","{true,false}"),("url_count","integer"),("hashtag_count","integer")]
    csv_to_arff('../dump/twitter_subset/evaluationEnriched2.csv', "result.arff", attributes)

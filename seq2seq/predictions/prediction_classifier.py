import sys

def main(buggy, fixed, prediction):
    
    count_perfect = 0
    count_changed = 0
    count_bad = 0

    file_buggy = open(buggy, 'r')
    file_fixed = open(fixed, 'r')
    file_prediction = open(prediction, 'r')
    
    for line in file_buggy:
        buggy_line = line.strip()
        fixed_line = file_fixed.readline().strip()
        prediction_line = file_prediction.readline().strip()
        
        if(fixed_line == prediction_line):
            count_perfect += 1
        
        elif(buggy_line == prediction_line):
            count_bad += 1

        else:
            count_changed += 1

    file_buggy.close()
    file_fixed.close()
    file_prediction.close()
    
    sys.exit((str(count_perfect) + " " + str(count_changed) + " " + str(count_bad)))

if __name__=="__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])

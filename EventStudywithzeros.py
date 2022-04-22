import statistics
from scipy.stats import linregress
import pandas
import math
import os
import csv


class eventstudy:
    bse = []  # for 100 days data
    infotech = []  # for company data
    date_100 = []  # for days count
    bse_40 = []  # for 40 days
    infotech_40 = []  # for 40 days company data
    dates_40 = []  # for 40 days count
    ranges = 200  # range after examine days
    examine = 20  # examine period
    days_100 = []  # for storing date large
    days_40 = []  # for storing 40 dates

    @staticmethod
    # for reducing date
    def date_reducer(test):
        splitter = test.split('/')
        day = int(splitter[0])
        month = (splitter[1])
        if 1 < day <= 10:
            temps = "0" + str(day - 1) + '/' + '/'.join(splitter[1:])
        elif day > 10:
            temps = str(day - 1) + '/' + '/'.join(splitter[1:])
        elif day == 1:
            if month == "01":
                temps = "31/12/" + str(int(splitter[2]) - 1)
            elif month == "03":
                temps = "28" + "/02/" + splitter[2]
            elif month == "05" or month == "07" or month == "08" or month == "10":
                temps = "30/" + "0" + str(int(month) - 1) + '/' + splitter[2]
            elif month == "02" or month == "04" or month == "06" or month == "09":
                temps = "31/" + "0" + str(int(month) - 1) + '/' + splitter[2]
            elif int(month) > 10:
                if month == "11":
                    temps = "31" + "/10/" + splitter[2]
                elif month == "12":
                    temps = "30" + "/11/" + splitter[2]

        return temps  # for re

    @staticmethod
    # for generating window  file
    def file_generator(array, standard_dev, filename):
        t1 = ""
        t2 = ""
        t3 = ""
        t4 = ""
        t5 = ""
        t6 = ""
        t7 = ""
        for i in range(7):  # window calculation
            if i == 0:
                ar = array[20]
                day = 1
                squn = math.sqrt(day)
                t = (ar / standard_dev) * squn
                t1 += (str("Day_0") + " " + str(ar) + " " + str(day) + " " + str(squn) + " " + str(
                    standard_dev) + " " + str(t))
            elif i == 1:
                ar = array[19:21]
                day = len(ar)
                squn = math.sqrt(day)
                t = (sum(ar) / standard_dev) * squn
                t2 += (str("Min_1_to_0") + " " + str(sum(ar)) + " " + str(day) + " " + str(squn) + " " + str(
                    standard_dev) + " " + str(t))

            elif i == 2:
                ar = (array[19:22])
                day = len(ar)
                squn = math.sqrt(day)
                t = (sum(ar) / standard_dev) * squn
                t3 += (str("Min_1_to_plus_1") + " " + str(sum(ar)) + " " + str(day) + " " + str(squn) + " " + str(
                    standard_dev) + " " + str(t))

            elif i == 3:
                ar = (array[20:31])
                day = len(ar)
                squn = math.sqrt(day)
                t = (sum(ar) / standard_dev) * squn
                t4 += (str("0_to_plus_10") + " " + str(sum(ar)) + " " + str(day) + " " + str(squn) + " " + str(
                    standard_dev) + " " + str(t))

            elif i == 4:
                ar = (array[10:21])
                day = len(ar)
                squn = math.sqrt(day)
                t = (sum(ar) / standard_dev) * squn
                t5 += (str("0_to_minus_10") + " " + str(sum(ar)) + " " + str(day) + " " + str(squn) + " " + str(
                    standard_dev) + " " + str(t))

            elif i == 5:
                ar = (array[10:31])
                day = len(ar)
                squn = math.sqrt(day)
                t = (sum(ar) / standard_dev) * squn
                t6 += (str("Minus_10_to_plus_10") + " " + str(sum(ar)) + " " + str(day) + " " + str(squn) + " " + str(
                    standard_dev) + " " + str(t))

            elif i == 6:
                ar = (array[:])
                day = len(ar)
                squn = math.sqrt(day)
                t = (sum(ar) / standard_dev) * squn
                t7 += (str("Minus_20_to_plus_20") + " " + str(sum(ar)) + " " + str(day) + " " + str(squn) + " " + str(
                    standard_dev) + " " + str(t))

        import csv
        fields = ['Window', 'CAR', 'Days', 'SQU_N', "STDDEV", 'T', "significance"]
        # data rows of csv file
        rows = [t1.split(" "),
                t2.split(" "),
                t3.split(" "), t4.split(" "),
                t5.split(" "), t6.split(" "), t7.split(" ")]

        with open(filename, 'w') as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)

            # writing the fields
            csvwriter.writerow(fields)

            # writing the data rows
            csvwriter.writerows(rows)

    @staticmethod
    # for cumulative file generation
    def cumulative_file_generator(date_100, estimation_return_mean_100, file_cummulative, start_date,demo_number):
        if company_number == 0:
            with open(os.path.join(directory, file_cummulative), 'w',newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(["days", company_name])
                csvwriter.writerow(["Anouncement Dates",start_date])
                csvwriter.writerow(["Demo Number", demo_number])
                for i in range(len(date_100)):
                    csvwriter.writerow([date_100[i], estimation_return_mean_100[i]])
        elif company_number > 0:
            k = []
            with open(os.path.join(directory, file_cummulative), newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in spamreader:
                    k.append(row)
            for i in range(len(k)):
                if i == 0:
                    k[i].append(company_name)
                elif i==1:
                    k[i].append(start_date)
                elif i == 2:
                    k[i].append(demo_number)
                else:
                    k[i].append(estimation_return_mean_100[i - 3])
            with open(os.path.join(directory, file_cummulative), 'w',newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerows(k)

    @staticmethod
    # for generating mean adjusted model
    def mean_adjusted_model(bse, infotech, bse_40, infotech_40, date_100, dates_40, days_100, days_40,start_date,demo_number):
        if len(infotech) == infotech.count(" "):
            print("Cannot Compute Mean Adjusted Model for ", company_name, "due to blank Data")
            return
        estimation_mean = statistics.mean(infotech)  # mean caluclation for mean adjusted model
        estimation_return_mean_100 = []
        actual_return_mean_40 = []
        for i in range(len(infotech)):
            estimation_return_mean_100.append(
                infotech[i] - estimation_mean)  # estimated return for 100 values(infotech-estimation_mean)
        for i in range(len(infotech_40)):
            actual_return_mean_40.append(
                infotech_40[i] - estimation_mean)  # estimated return for 100 values(infotech-estimation_mean)
        stadard_mean_adjusted_dev_100 = statistics.stdev(
            estimation_return_mean_100)  # standard deviation of 100 estimated return mean
        cars_40_mean_adjusted_model = []
        for i in range(len(actual_return_mean_40)):  # CAR value for mean adjusted model
            if i == 0:
                cars_40_mean_adjusted_model.append(actual_return_mean_40[i])
            else:
                cars_40_mean_adjusted_model.append(cars_40_mean_adjusted_model[i - 1] + actual_return_mean_40[i])
        file_1001 = "Estimations-Mean-adjusted-model" + ".csv"
        with open(os.path.join(directory, file_1001), '+a',newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([company_name])
            csvwriter.writerow(["Date", "BSE", company_name, "Predicted return", "Estimated returns"])
            for i in range(len(bse)):
                csvwriter.writerow(
                    [str(days_100[i]), str(bse[i]), str(infotech[i]), str(estimation_mean),
                     str(estimation_return_mean_100[i])])
            csvwriter.writerow(["standard deviation " + company_name + ":", stadard_mean_adjusted_dev_100])
            csvwriter.writerow("\n")
            csvwriter.writerow("\n")
            csvwriter.writerow("\n")

        file_40 = "mean-adjusted-model[40]"  + ".csv"
        with open(os.path.join(directory, file_40), '+a',newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([company_name])
            csvwriter.writerow(["Date", "BSE", company_name, "Predicted return", "Abnormal Return", "Days", "CAR"])
            for i in range(len(bse_40)):
                csvwriter.writerow(
                    [str(days_40[i]), str(bse_40[i]), str(infotech_40[i]), str(estimation_mean),
                     str(actual_return_mean_40[i]),
                     str(dates_40[i]), str(cars_40_mean_adjusted_model[i])])

            csvwriter.writerow(["standard deviation " + company_name + ":", stadard_mean_adjusted_dev_100])
            csvwriter.writerow("\n")
            csvwriter.writerow("\n")
            csvwriter.writerow("\n")

        file_cummulative = "mean-adjusted-model-cumulative" + ".csv"
        file_cummulative_40 = "mean-adjusted-model_cumulative_40"  + ".csv"

        eventstudy.cumulative_file_generator(date_100, estimation_return_mean_100, file_cummulative,start_date,demo_number)
        eventstudy.cumulative_file_generator(dates_40, actual_return_mean_40, file_cummulative_40,start_date,demo_number)

    @staticmethod
    # for generating market model
    def market_model(bse, infotech, bse_40, infotech_40, date_100, dates_40, days_100, days_40,start_date,demo_number):
        if len(bse)==bse.count(" "):
            print("Cannot compute Market Model for ",company_name,"due to blank data")
            return
        beta = linregress(bse, infotech)[0]  # beta value
        alpha = linregress(bse, infotech)[1]  # alpha value
        predicted_return = []
        abnormal_return_40 = []
        cars_40 = []
        expected_return = []
        abnormal_return = []
        for i in range(len(bse)):  # caluclation of expected and abnormal values
            t = alpha + (beta * bse[i])
            expected_return.append(t)
            abnormal_return.append(infotech[i] - t)
        stadard_dev_100 = (statistics.stdev(abnormal_return))  # standard deviation of market model
        for i in range(len(bse_40)):  # predicted and abnormal return calculation for market model
            t = alpha + (beta * bse_40[i])
            predicted_return.append(t)
            abnormal_return_40.append((infotech_40[i] - t))
        for i in range(len(bse_40)):  # CAR
            if i == 0:
                cars_40.append(abnormal_return_40[i])
            else:
                cars_40.append(cars_40[i - 1] + abnormal_return_40[i])

        file_100 = "Estimations-Market-Model"  + ".csv"
        with open(os.path.join(directory, file_100), '+a',newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([company_name])
            csvwriter.writerow(["Date", "BSE", company_name, "Expected return", "Abnormal return"])
            for i in range(len(bse)):
                csvwriter.writerow(
                    [str(days_100[i]), str(bse[i]), str(infotech[i]), str(expected_return[i]), str(abnormal_return[i])])
            csvwriter.writerow(["alpha " + company_name + ":", alpha])
            csvwriter.writerow(["beta " + company_name + ":", beta])
            csvwriter.writerow("\n")
            csvwriter.writerow("\n")

        file_40 = "market-model[40]"  + ".csv"
        with open(os.path.join(directory, file_40), '+a',newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Date", "BSE", company_name, "Predicted return", "AR", "Days", "CAR"])
            for i in range(len(bse_40)):
                csvwriter.writerow(
                    [str(days_40[i]), str(bse_40[i]), str(infotech_40[i]), str(predicted_return[i]),
                     str(abnormal_return_40[i]),
                     str(dates_40[i]), str(cars_40[i])])
            csvwriter.writerow(["alpha " + company_name + ":", alpha])
            csvwriter.writerow(["beta " + company_name + ":", beta])
            csvwriter.writerow(["standard deviation " + company_name, stadard_dev_100])

        file_cummulative = "Market-model-cumulative" + ".csv"
        file_cummulative_40 = "Market-model-cumulative_40" + ".csv"

        eventstudy.cumulative_file_generator(date_100, abnormal_return, file_cummulative,start_date,demo_number)
        eventstudy.cumulative_file_generator(dates_40, abnormal_return_40, file_cummulative_40,start_date,demo_number)

    @staticmethod
    # for generating market adjusted model
    def market_adjusted_model(bse, infotech, bse_40, infotech_40, date_100, dates_40, days_100, days_40,start_date,demo_number):
        mean_bse_100 = statistics.mean(bse)  # mean calculation for market adjusted model
        estimation_period_return = []
        for i in range(len(infotech)):  # estimation period return for 100 days
            estimation_period_return.append(infotech[i] - mean_bse_100)
        if (len(estimation_period_return)==estimation_period_return.count(' ')):
            print(" Cannot compute Market Adjusted model for ",company_name,"due to blank data")
            return 0
        stadard_dev_market_adjusted_model = statistics.stdev(
            estimation_period_return)  # standard deviation for estimated return
        actual_return_mean_40_mam = []
        for i in range(len(infotech_40)):  # estimation for 40 days
            actual_return_mean_40_mam.append(infotech_40[i] - mean_bse_100)
        cars_40_mam = []
        for i in range(len(actual_return_mean_40_mam)):  # CAR calculation
            if i == 0:
                cars_40_mam.append(actual_return_mean_40_mam[i])
            else:
                cars_40_mam.append(+cars_40_mam[i - 1] + actual_return_mean_40_mam[i])
        file_1001 = "Estimations-Market-adjusted-model"+ ".csv"
        with open(os.path.join(directory, file_1001), '+a',newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([company_name])
            csvwriter.writerow(["Date", "BSE", company_name, "Predicted return", "Estimated returns"])
            for i in range(len(bse)):
                csvwriter.writerow(
                    [str(days_100[i]), str(bse[i]), str(infotech[i]), str(mean_bse_100),
                     str(estimation_period_return[i])])
            csvwriter.writerow(["standard deviation " + company_name + ":", stadard_dev_market_adjusted_model])
            csvwriter.writerow("\n\n\n")

        file_40 = "Market-adjusted-model[40]" + ".csv"
        with open(os.path.join(directory, file_40), '+a',newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Date", "BSE", company_name, "Predicted return", "Abnormal Return", "Days", "CAR"])
            for i in range(len(bse_40)):
                csvwriter.writerow(
                    [str(days_40[i]), str(bse_40[i]), str(infotech_40[i]), str(mean_bse_100),
                     str(actual_return_mean_40_mam[i]),
                     str(dates_40[i]), str(cars_40_mam[i])])

            csvwriter.writerow(["standard deviation " + company_name + ":", stadard_dev_market_adjusted_model])
            csvwriter.writerow("\n\n\n")

        file_cummulative = "Market-adjusted-model-cumulative" + ".csv"
        file_cummulative_40 = "Market-adjusted-model-cumulative_40" + ".csv"

        eventstudy.cumulative_file_generator(date_100, estimation_period_return, file_cummulative,start_date,demo_number)
        eventstudy.cumulative_file_generator(dates_40, actual_return_mean_40_mam, file_cummulative_40,start_date,demo_number)

    @staticmethod
    # Calling function
    def extractor_function(start_date, company_name,demo_number):
        date = data['Date'].tolist()[1:].index(start_date)  # finding the index of date
        for i in range(date - eventstudy.ranges - eventstudy.examine +1,
                       date - eventstudy.examine +1):  # for converting string data to float for the -121 to -21 date
            eventstudy.bse.append(float(data['bse'].tolist()[i]))
            eventstudy.date_100.append(date - i - eventstudy.examine+1)
            eventstudy.days_100.append((data['Date'].tolist()[i]))
            if str(data[company_name].tolist()[i]) != " ":
                eventstudy.infotech.append(float(data[company_name].tolist()[i]))
            elif (str(data[company_name].tolist()[i])) == " ":
                eventstudy.infotech.append(float(0))

        for i in range(date - eventstudy.examine+1,
                       date + eventstudy.examine + 2):  # for converting string data to float for the -20 to +20 date
            eventstudy.bse_40.append(float(data['bse'].tolist()[i]))
            eventstudy.dates_40.append(i - date-1)
            eventstudy.days_40.append((data['Date'].tolist()[i]))
            if str(data[company_name].tolist()[i]) != " ":
                eventstudy.infotech_40.append(float(data[company_name].tolist()[i]))
            elif (str(data[company_name].tolist()[i])) == " ":
                eventstudy.infotech_40.append(float(0))


        eventstudy.market_adjusted_model(eventstudy.bse, eventstudy.infotech, eventstudy.bse_40
                                         , eventstudy.infotech_40, eventstudy.date_100, eventstudy.dates_40,
                                         eventstudy.days_100, eventstudy.days_40,start_date,demo_number)

        eventstudy.market_model(eventstudy.bse, eventstudy.infotech, eventstudy.bse_40
                                , eventstudy.infotech_40, eventstudy.date_100, eventstudy.dates_40, eventstudy.days_100,
                                eventstudy.days_40,start_date,demo_number)

        eventstudy.mean_adjusted_model(eventstudy.bse, eventstudy.infotech, eventstudy.bse_40
                                       , eventstudy.infotech_40, eventstudy.date_100, eventstudy.dates_40,
                                       eventstudy.days_100, eventstudy.days_40,start_date,demo_number)

        eventstudy.bse = []
        eventstudy.infotech = []
        eventstudy.bse_40 = []
        eventstudy.date_100 = []
        eventstudy.dates_40 = []
        eventstudy.infotech_40 = []
        eventstudy.days_100 = []
        eventstudy.days_40 = []
        print("Done for " + company_name)


datafile = 'testfile.csv'  # data file
directory = r'C:\Users\shrey\Desktop\event'
# data directory
anouncement_dates_company = 'anouncement_dates.csv'  # list of companies and their announcement date
data = pandas.read_csv(os.path.join(directory, datafile), delimiter=",")  # reading data from datafile
company_data = pandas.read_csv(os.path.join(directory, anouncement_dates_company),
                               delimiter=",")  # reading data about companies and their anouncement
companies_name = list(company_data["Company Name"])  # list for company name
anouncement_dates = list(company_data["Ann date"])  # list for company anouncement date
demo=list(company_data["Deal number"])  # list for company Demo date
event = eventstudy()  # object for eventstudy class
for company_number in range(len(companies_name)):  # running for each company
    company_name = companies_name[company_number]  # for company
    if not data.columns.tolist().__contains__(company_name):
        print('Company name',company_name, 'not in',datafile)
        continue
    temp = anouncement_dates[company_number]  # for company anouncement date
    demo_number=demo[company_number]
    temp1=event.date_reducer(temp)
    temp2=event.date_reducer(temp1)
    if temp in list(data['Date']):
        if data['Date'].tolist()[1:].index(temp)!=" ":
            date=data['Date'].tolist()[1:].index(temp)
            event.extractor_function(temp, company_name, demo_number)
    elif temp1 in list(data['Date']):
        date=data['Date'].tolist()[1:].index(temp1)
        event.extractor_function(temp1, company_name, demo_number)
    elif temp2 in list(data['Date']):
        date=data['Date'].tolist()[1:].index(temp2)
        event.extractor_function(temp2, company_name, demo_number)
    else:
        print("Can't do for" + company_name)

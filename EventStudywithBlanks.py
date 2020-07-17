import statistics
from scipy.stats import linregress
import pandas
import math
import os
import csv


class eventstudy:
    bse = []  # for 100 days data
    bse_market_model = []  # for bse values in the market model where companies data exist
    infotech_market_model = []  # for company values in the market model where value are not blanks
    infotech_mean_adjusted_model = []  # for company values in the mean adjusted model where value are not blanks
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
    # for generating the combined file
    def cummulative_file_generator(date_100, estimation_return_mean_100, file_cummulative):
        if company_number == 0:
            with open(os.path.join(directory, file_cummulative), 'w') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(["days", company_name])
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
                else:
                    k[i].append(estimation_return_mean_100[i - 1])
            with open(os.path.join(directory, file_cummulative), 'w') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerows(k)

    @staticmethod
    # for generating mean adjusted model
    def mean_adjusted_model(bse, infotech, bse_40, infotech_40, date_100, dates_40, days_100, days_40
                            , infotech_mean_adjusted_model):
        estimation_mean = statistics.mean(infotech_mean_adjusted_model)  # mean calculation for mean adjusted model
        estimation_return_mean_100 = []
        estimation_return_mean_100_stdev = []
        actual_return_mean_40 = []
        for i in range(len(infotech)):
            if infotech[i] != " ":
                estimation_return_mean_100_stdev.append(infotech[i] - estimation_mean)
                estimation_return_mean_100.append(
                    infotech[i] - estimation_mean)  # estimated return for 100 values(infotech-estimation_mean)
            elif infotech[i] == " ":
                estimation_return_mean_100.append(" ")
        for i in range(len(infotech_40)):
            if infotech_40[i] != " ":
                actual_return_mean_40.append(
                    infotech_40[i] - estimation_mean)  # estimated return for 100 values(infotech-estimation_mean)
            elif infotech_40[i] == " ":
                actual_return_mean_40.append(" ")

        stadard_mean_adjusted_dev_100 = statistics.stdev(
            estimation_return_mean_100_stdev)  # standard deviation of 100 estimated return mean

        file_1001 = "Blank-Estimations-Mean-adjusted-model" + "".join(companies_name) + ".csv"
        with open(os.path.join(directory, file_1001), '+a') as csvfile:
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

        file_40 = "Blank-mean-adjusted-model[40]" + "".join(companies_name) + ".csv"
        with open(os.path.join(directory, file_40), '+a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([company_name])
            csvwriter.writerow(["Date", "BSE", company_name, "Predicted return", "Abnormal Return", "Days"])
            for i in range(len(bse_40)):
                csvwriter.writerow(
                    [str(days_40[i]), str(bse_40[i]), str(infotech_40[i]), str(estimation_mean),
                     str(actual_return_mean_40[i]),
                     str(dates_40[i])])

            csvwriter.writerow(["standard deviation " + company_name + ":", stadard_mean_adjusted_dev_100])
            csvwriter.writerow("\n")
            csvwriter.writerow("\n")
            csvwriter.writerow("\n")

        file_cummulative = "Blank-mean-adjusted-model-cumulative" + "".join(companies_name) + ".csv"
        file_cummulative_40 = "Blank-mean-adjusted-model_cumulative_40" + "".join(companies_name) + ".csv"

        eventstudy.cummulative_file_generator(date_100, estimation_return_mean_100, file_cummulative)
        eventstudy.cummulative_file_generator(dates_40, actual_return_mean_40, file_cummulative_40)

    @staticmethod
    # for generating market model
    def market_model(bse, infotech, bse_40, infotech_40, date_100, dates_40, days_100, days_40, infotech_market_model
                     , bse_market_model):
        beta = linregress(bse_market_model, infotech_market_model)[0]  # beta value
        alpha = linregress(bse_market_model, infotech_market_model)[1]  # alpha value
        predicted_return = []
        abnormal_return_40 = []
        expected_return = []
        abnormal_return = []
        abnormal_return_stdev = []
        for i in range(len(bse)):  # caluclation of expected and abnormal values
            t = alpha + (beta * bse[i])
            expected_return.append(t)
            if infotech[i] != " ":
                abnormal_return.append(infotech[i] - t)
                abnormal_return_stdev.append(infotech[i] - t)
            elif infotech[i] == " ":
                abnormal_return.append(" ")
        stadard_dev_100 = (statistics.stdev(abnormal_return_stdev))  # standard deviation of market model
        for i in range(len(bse_40)):  # predicted and abnormal return calculation for market model
            t = alpha + (beta * bse_40[i])
            predicted_return.append(t)
            if infotech_40[i] != " ":
                abnormal_return_40.append((infotech_40[i] - t))
            elif infotech_40[i] == " ":
                abnormal_return_40.append(" ")

        file_100 = "blank-Estimations-Market-Model" + "".join(companies_name) + ".csv"
        with open(os.path.join(directory, file_100), '+a') as csvfile:
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
        #
        file_40 = "blank-market-model[40]" + "".join(companies_name) + ".csv"
        with open(os.path.join(directory, file_40), '+a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Date", "BSE", company_name, "Predicted return", "AR", "Days"])
            for i in range(len(bse_40)):
                csvwriter.writerow(
                    [str(days_40[i]), str(bse_40[i]), str(infotech_40[i]), str(predicted_return[i]),
                     str(abnormal_return_40[i]),
                     str(dates_40[i])])
            csvwriter.writerow(["alpha " + company_name + ":", alpha])
            csvwriter.writerow(["beta " + company_name + ":", beta])
            csvwriter.writerow(["standard deviation " + company_name, stadard_dev_100])

        file_cummulative = "Blank-Market-model-cumulative" + "".join(companies_name) + ".csv"
        file_cummulative_40 = "Blank-Market-model-cumulative-_40" + "".join(companies_name) + ".csv"

        eventstudy.cummulative_file_generator(date_100, abnormal_return, file_cummulative)
        eventstudy.cummulative_file_generator(dates_40, abnormal_return_40, file_cummulative_40)

    @staticmethod
    # for generating market adjusted model
    def market_adjusted_model(bse, infotech, bse_40, infotech_40, date_100, dates_40, days_100, days_40):
        mean_bse_100 = statistics.mean(bse)  # mean calculation for market adjusted model
        estimation_period_return = []
        estimation_period_return_stdev = []
        for i in range(len(infotech)):  # estimation period return for 100 days
            if infotech[i] != ' ':
                estimation_period_return.append(infotech[i] - mean_bse_100)
                estimation_period_return_stdev.append(infotech[i] - mean_bse_100)
            elif infotech[i] == " ":
                estimation_period_return.append(" ")
        stadard_dev_market_adjusted_model = statistics.stdev(
            estimation_period_return_stdev)  # standard deviation for estimated return
        actual_return_mean_40_mam = []
        for i in range(len(infotech_40)):  # estimation for 40 days
            if infotech_40[i] != " ":
                actual_return_mean_40_mam.append(infotech_40[i] - mean_bse_100)
            else:
                actual_return_mean_40_mam.append(" ")
        file_1001 = "Blank-Estimations-Market-adjusted-model" + "".join(companies_name) + ".csv"
        with open(os.path.join(directory, file_1001), '+a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([company_name])
            csvwriter.writerow(["Date", "BSE", company_name, "Predicted return", "Estimated returns"])
            for i in range(len(bse)):
                csvwriter.writerow(
                    [str(days_100[i]), str(bse[i]), str(infotech[i]), str(mean_bse_100),
                     str(estimation_period_return[i])])
            csvwriter.writerow(["standard deviation " + company_name + ":", stadard_dev_market_adjusted_model])
            csvwriter.writerow("\n\n\n")

        file_40 = "Blank-Market-adjusted-model_[40]" + "".join(companies_name) + ".csv"
        with open(os.path.join(directory, file_40), '+a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Date", "BSE", company_name, "Predicted return", "Abnormal Return", "Days"])
            for i in range(len(bse_40)):
                csvwriter.writerow(
                    [str(days_40[i]), str(bse_40[i]), str(infotech_40[i]), str(mean_bse_100),
                     str(actual_return_mean_40_mam[i]),
                     str(dates_40[i])])

            csvwriter.writerow(["standard deviation " + company_name + ":", stadard_dev_market_adjusted_model])
            csvwriter.writerow("\n\n\n")

        file_cummulative = "Blank-Market-adjusted-model-cumulative_" + "".join(companies_name) + ".csv"
        file_cummulative_40 = "Blank-Market-adjusted-model-cumulative_40" + "".join(companies_name) + ".csv"
        eventstudy.cummulative_file_generator(date_100, estimation_period_return, file_cummulative)
        eventstudy.cummulative_file_generator(dates_40, actual_return_mean_40_mam, file_cummulative_40)

    @staticmethod
    # Calling function
    def extractor_function(start_date, company_name):
        date = data['Date'].tolist()[1:].index(start_date)  # finding the index of date
        print()
        for i in range(date - eventstudy.ranges - eventstudy.examine + 1,
                       date - eventstudy.examine + 1):  # for converting string data to float for the -121 to -21 date

            if str(data[company_name].tolist()[i]) != " ":
                eventstudy.infotech.append(float(data[company_name].tolist()[i]))
                eventstudy.bse.append(float(data['bse'].tolist()[i]))
                eventstudy.infotech_market_model.append(float(data[company_name].tolist()[i]))
                eventstudy.infotech_mean_adjusted_model.append(float(data[company_name].tolist()[i]))
                eventstudy.bse_market_model.append(float(data['bse'].tolist()[i]))
                eventstudy.date_100.append(date - i - eventstudy.examine + 1)
                eventstudy.days_100.append((data['Date'].tolist()[i]))
            elif (str(data[company_name].tolist()[i])) == " ":
                eventstudy.infotech.append(" ")
                eventstudy.bse.append(float(data['bse'].tolist()[i]))
                eventstudy.date_100.append(date - i - eventstudy.examine + 1)
                eventstudy.days_100.append((data['Date'].tolist()[i]))
        for i in range(date - eventstudy.examine + 1,
                       date + eventstudy.examine + 2):  # for converting string data to float for the -20 to +20 date
            if str(data[company_name].tolist()[i]) != " ":
                eventstudy.infotech_40.append(float(data[company_name].tolist()[i]))
                eventstudy.bse_40.append(float(data['bse'].tolist()[i]))
                eventstudy.dates_40.append(i - date - 1)
                eventstudy.days_40.append((data['Date'].tolist()[i]))
            elif (str(data[company_name].tolist()[i])) == " ":
                eventstudy.infotech_40.append(" ")
                eventstudy.bse_40.append(float(data['bse'].tolist()[i]))
                eventstudy.dates_40.append(i - date - 1)
                eventstudy.days_40.append((data['Date'].tolist()[i]))

        eventstudy.market_adjusted_model(eventstudy.bse, eventstudy.infotech, eventstudy.bse_40
                                         , eventstudy.infotech_40, eventstudy.date_100, eventstudy.dates_40,
                                         eventstudy.days_100, eventstudy.days_40)

        eventstudy.market_model(eventstudy.bse, eventstudy.infotech, eventstudy.bse_40
                                , eventstudy.infotech_40, eventstudy.date_100, eventstudy.dates_40, eventstudy.days_100,
                                eventstudy.days_40, eventstudy.bse_market_model, eventstudy.infotech_market_model)

        eventstudy.mean_adjusted_model(eventstudy.bse, eventstudy.infotech, eventstudy.bse_40
                                       , eventstudy.infotech_40, eventstudy.date_100, eventstudy.dates_40,
                                       eventstudy.days_100, eventstudy.days_40, eventstudy.infotech_mean_adjusted_model)

        eventstudy.bse = []
        eventstudy.infotech = []
        eventstudy.bse_40 = []
        eventstudy.date_100 = []
        eventstudy.dates_40 = []
        eventstudy.infotech_40 = []
        eventstudy.days_100 = []
        eventstudy.days_40 = []
        eventstudy.bse_market_model = []
        eventstudy.infotech_market_model = []
        eventstudy.infotech_mean_adjusted_model = []
        print("Done for " + company_name)


datafile = ''  # data file
directory = ''  # data directory
anouncement_dates_company = ''  # list of companies and their announcement date
data = pandas.read_csv(os.path.join(directory, datafile), delimiter=",")  # reading data from datafile
company_data = pandas.read_csv(os.path.join(directory, anouncement_dates_company),
                               delimiter=",")  # reading data about companies and their anouncement
companies_name = list(company_data["Company Name"])  # list for company name
anouncement_dates = list(company_data["Ann date"])  # list for company anouncement date

event = eventstudy()  # object for eventstudy class

for company_number in range(len(companies_name)):  # running for each company
    company_name = companies_name[company_number]  # for company
    temp = anouncement_dates[company_number]  # for company anouncement date
    if list(data['Date']).__contains__(temp):  # check for date if exist then good otherwise check for 2 days back
        date = data['Date'].tolist()[1:].index(temp)
        if (data[company_name].tolist()[date + 1] != " "):
            event.extractor_function(temp, company_name)
        elif (data[company_name].tolist()[date + 1] == " "):
            temp1 = event.date_reducer(temp)
            if list(data['Date']).__contains__(temp1):
                date = data['Date'].tolist()[1:].index(temp1)
                if (data[company_name].tolist()[date + 1] != " "):
                    event.extractor_function(temp1, company_name)
                elif (data[company_name].tolist()[date + 1] == " "):
                    temp2 = date_reducer(temp1)
                    if list(data['Date']).__contains__(temp2):
                        date = data['Date'].tolist()[1:].index(temp2)
                        if (data[company_name].tolist()[date + 1] != " "):
                            event.extractor_function(temp2, company_name)
                        else:
                            print("Can't do for" + company_name)

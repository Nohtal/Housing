
# coding: utf-8

# In[152]:

class Time:
    #number of years for your mortgage/investing horizon
    years = 30
    #number of months for your mortgage/investing horizon
    months = years * 12


class HousePrice:
    #price of a house you want to buy that isn't shit
    initial = 300000.0 
    
    downpayment = Capital.initial
    mortgage = [initial - downpayment] 
    final = [initial ]
    
class Capital:
    #initial amount of capital you have to invest
    initial = HousePrice.initial * 20/100
    #final capital over time period
    final = [initial]

class AnnualReturns:
    #average annual percent return of S&P500 over the last 30 years
    SPY = 10.0 
    #average annual percent return of S&P500 over the last 30 years
    personal = 25.0
                
class InterestRate:
    #monthly interest rate taken from WF 12/16/16->
    #interest compound methodology https://thefinancebuff.com/is-home-mortgage-simple-interest-or-compound-interest.html
    
    #annual bankloan interest rate
    bankLoanAnnual = 4.2
    
    #monthly bankloan interest rate
    bankLoan = ((1.0 + bankLoanAnnual/100)**(1.0 / 12.0) - 1.0) * 100
    
    #inflation rate over the past 30 years in USA
    inflation = 3.0
    
    #house appreciation rate over the past 26 years in los angeles-> https://www.neighborhoodscout.com/ca/los-angeles/rates/
    appreciation = 3.63

class Rent:
    #my initial rent in pasadena
    initial = 1300.0
    
    #Annual percent increase in rent
    increase = 3.78 
    
    #final rent after 30 years
    final = [initial]
    
    #total rent paid after 30 years
    total = []
    
class Cost:
    #monthly maintainence cost for a house
    maintain = HousePrice.initial*0.01/12.0 
    
    #annual property tax in los angeles->http://www.latimes.com/local/la-me-city-property-tax-table-htmlstory.html>
    propTax = HousePrice.initial*0.016
    
    #asim's monthly homeowner's insurance and earthquake insurance
    insurance = 2500.0/12.0 
    
    #calculating monthly mortgage from source using givens->https://goo.gl/0NxFrk
    mortgage = 1173.64
    
    #total mortgage paid over time period
    mortgageTotal = mortgage * Time.months
    
    #closing cost when house is bought ~4%
    boughtClosing = 0.04 * HousePrice.initial
    
    #total costs for owning a house fixed costs
    total = [boughtClosing ] 
    
#adjusting initial capital for opportunity cost of fees for buying a house
Capital.final[-1] = Capital.final[-1] + Cost.boughtClosing

# calculaing over a time period change in value for both strategies
for i in range(Time.months):   
    
#STOCK MARKET SRATEGY
    #creating the list of every month of rent paid over time period
    Rent.total.append(Rent.final[-1])
    
    #adjusting my capital for the opportunity costs of owning a house
    Capital.final[-1] = Capital.final[-1] + Cost.maintain + Cost.insurance
    
    #annual events
    choice = (i/12.0 - i//12.0)
    if i>0 and choice == 0: 
        #adding the opportunity costs of property tax
        Capital.final[-1] = Capital.final[-1]  + Cost.propTax*0.64
        
        #tracking the annual returns of my investment
        Capital.final.append(Capital.final[-1]*(1 + AnnualReturns.SPY/100))

        #defining the annual rent increase on a percent base of last paid rent
        Rent.final.append(Rent.final[-1] + Rent.final[-1] * Rent.increase/100)
        
        #paying taxes on my investment gains
#         Capital.final[-1] = Capital.final[-1] - (Capital.final[-1] - Capital.final[-2]) * 25/100
        
        #lowering the worth of my investment by the inflation rate
#         Capital.final[-1] = Capital.final[-1] - Capital.final[-1] * InterestRate.inflation/100       
    
#BUYING A HOUSE STRATEGY
    #making a list of all the hidden costs of owning a house
    Cost.total.append(Cost.maintain + Cost.insurance)
    
    #paying down the mortgage and interest
    HousePrice.mortgage.append(HousePrice.mortgage[-1]*(1 + InterestRate.bankLoan/100) - Cost.mortgage)

    #annual events
    choice = (i/12.0 - i//12.0)
    if i>0 and choice == 0:
        #total housing costs for the year including property tax after break and mortgage interest tax break
        Cost.total[-1] = Cost.total[-1] + Cost.propTax*0.64 - HousePrice.mortgage[-1]*InterestRate.bankLoan/100*0.25
        
        #adjusting the price of the house for appreciation
        HousePrice.final.append(HousePrice.final[-1] * (1 + (InterestRate.appreciation)/100))
         
        
#finding the total rent paid over a time period       
Rent.total.append(sum(Rent.total))

#the amount of interest paid on the house
Cost.total.append(sum(Cost.total) + ( Cost.mortgageTotal - HousePrice.initial))

#net liquid after selling your house after capital gains, selling costs, maintainence costs
HouseNetLiquid = HousePrice.final[-1] - HousePrice.final[-1] * 0.15 - HousePrice.final[-1] * 0.08 - Cost.total[-1] + Cost.mortgage*0.75*Time.months

#net Liquid after selling SPY
SPYtaxes = Capital.final[-1] * 0.15 
StockNetLiquid = Capital.final[-1] - Rent.total[-1] - SPYtaxes

print "***STOCK MARKET STRATEGY***"
print "The total paid rent over {} years is ${:,}.".format(Time.years, int(Rent.total[-1]))
print "The total return on investment over {} years is ${:,}.".format(Time.years, int(Capital.final[-1]))
print "The net liquid after selling your SPY stock over {} years is ${:,}.\n".format(Time.years, int(StockNetLiquid))

print "***BUYING A HOUSE STRATEGY***"
print "Final Appreciated price of your house in {} years is ${:,}.".format(Time.years, int(HousePrice.final[-1]))
print "Cost for owning your house after {} years are ${:,}.".format(Time.years, int(Cost.total[-1]))
print "Amount of interest you pay over a {} year loan is ${:,}.".format(Time.years, -int(HousePrice.initial - Cost.mortgageTotal))
print "The net liquid after selling your house over {} years is ${:,}.".format(Time.years, int(HouseNetLiquid))

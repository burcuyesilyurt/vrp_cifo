import random
from random import sample

from charles.charles import Population, Individual
from charles.selection import fps, tournament_sel
from charles.mutation import swap_mutation, inversion_mutation
from charles.xo import cycle_xo, pmx, vrp_pmx, vrp_single_point_xo
from fitness_functions import get_fitness
from initializations import random_initialization

data = [
    #0
    ['D0', 'd', '40.0', '50.0', '0.0', '0.0', '1236.0', '0.0', '0'],
    #1
    ['S0', 'f', '40.0', '50.0', '0.0', '0.0', '1236.0', '0.0', '0'],
    #2
    ['S15', 'f', '39.0', '26.0', '0.0', '0.0', '1236.0', '0.0', '0'],
    #3
    ['C20', 'cd', '30.0', '50.0', '-10.0', '0.0', '1136.0', '90.0', 'C99'],
    #4
    ['C24', 'cd', '25.0', '50.0', '-20.0', '0.0', '1131.0', '90.0', 'C65'],
    #5
    ['C57', 'cd', '40.0', '15.0', '-60.0', '989.0', '1063.0', '90.0', 'C98'],
    #6
    ['C65', 'cp', '48.0', '40.0', '20.0', '67.0', '139.0', '90.0', 'C24'],
    #7
    ['C98', 'cp', '58.0', '75.0', '60.0', '0.0', '1115.0', '90.0', 'C57'],
    #8
    ['C99', 'cp', '30.0', '50.0', '10.0', '0.0', '1136.0', '0.0', 'C20']
]

data = [['D0', 'd', '40.0', '50.0', '0.0', '0.0', '240.0', '0.0', '0'], ['S0', 'f', '40.0', '50.0', '0.0', '0.0', '240.0', '0.0', '0'], ['S1', 'f', '73.0', '52.0', '0.0', '0.0', '240.0', '0.0', '0'], ['S2', 'f', '90.0', '55.0', '0.0', '0.0', '240.0', '0.0', '0'], ['S3', 'f', '55.0', '79.0', '0.0', '0.0', '240.0', '0.0', '0'], ['S4', 'f', '69.0', '89.0', '0.0', '0.0', '240.0', '0.0', '0'], ['S5', 'f', '32.0', '80.0', '0.0', '0.0', '240.0', '0.0', '0'], ['S6', 'f', '39.0', '96.0', '0.0', '0.0', '240.0', '0.0', '0'], ['S7', 'f', '23.0', '80.0', '0.0', '0.0', '240.0', '0.0', '0'], ['S8', 'f', '4.0', '83.0', '0.0', '0.0', '240.0', '0.0', '0'], ['S9', 'f', '18.0', '58.0', '0.0', '0.0', '240.0', '0.0', '0'], ['S10', 'f', '1.0', '56.0', '0.0', '0.0', '240.0', '0.0', '0'], ['S11', 'f', '13.0', '31.0', '0.0', '0.0', '240.0', '0.0', '0'], ['S12', 'f', '-5.0', '38.0', '0.0', '0.0', '240.0', '0.0', '0'], ['S13', 'f', '26.0', '37.0', '0.0', '0.0', '240.0', '0.0', '0'], ['S14', 'f', '28.0', '13.0', '0.0', '0.0', '240.0', '0.0', '0'], ['S15', 'f', '39.0', '31.0', '0.0', '0.0', '240.0', '0.0', '0'], ['S16', 'f', '48.0', '11.0', '0.0', '0.0', '240.0', '0.0', '0'], ['S17', 'f', '59.0', '17.0', '0.0', '0.0', '240.0', '0.0', '0'], ['S18', 'f', '73.0', '23.0', '0.0', '0.0', '240.0', '0.0', '0'], ['S19', 'f', '74.0', '32.0', '0.0', '0.0', '240.0', '0.0', '0'], ['S20', 'f', '90.0', '44.0', '0.0', '0.0', '240.0', '0.0', '0'], ['C1', 'cp', '25.0', '85.0', '20.0', '145.0', '175.0', '0.0', 'C105'], ['C2', 'cd', '22.0', '75.0', '-10.0', '50.0', '80.0', '10.0', 'C45'], ['C3', 'cd', '22.0', '85.0', '-10.0', '109.0', '139.0', '10.0', 'C8'], ['C4', 'cd', '20.0', '80.0', '-20.0', '141.0', '171.0', '10.0', 'C5'], ['C5', 'cp', '20.0', '85.0', '20.0', '41.0', '71.0', '10.0', 'C4'], ['C6', 'cd', '18.0', '75.0', '-20.0', '95.0', '125.0', '10.0', 'C7'], ['C7', 'cp', '15.0', '75.0', '20.0', '79.0', '109.0', '10.0', 'C6'], ['C8', 'cp', '15.0', '80.0', '10.0', '91.0', '121.0', '10.0', 'C3'], ['C9', 'cp', '10.0', '35.0', '20.0', '91.0', '121.0', '10.0', 'C13'], ['C10', 'cp', '10.0', '40.0', '30.0', '119.0', '149.0', '10.0', 'C17'], ['C11', 'cp', '8.0', '40.0', '40.0', '59.0', '89.0', '10.0', 'C15'], ['C12', 'cp', '8.0', '45.0', '20.0', '64.0', '94.0', '10.0', 'C46'], ['C13', 'cd', '5.0', '35.0', '-20.0', '142.0', '172.0', '10.0', 'C9'], ['C14', 'cp', '5.0', '45.0', '10.0', '35.0', '65.0', '10.0', 'C47'], ['C15', 'cd', '2.0', '40.0', '-40.0', '58.0', '88.0', '10.0', 'C11'], ['C16', 'cd', '0.0', '40.0', '-9.0', '72.0', '102.0', '10.0', 'C82'], ['C17', 'cd', '0.0', '45.0', '-30.0', '149.0', '179.0', '10.0', 'C10'], ['C18', 'cd', '44.0', '5.0', '-40.0', '87.0', '117.0', '10.0', 'C19'], ['C19', 'cp', '42.0', '10.0', '40.0', '72.0', '102.0', '10.0', 'C18'], ['C20', 'cd', '42.0', '15.0', '-10.0', '122.0', '152.0', '10.0', 'C49'], ['C21', 'cd', '40.0', '5.0', '-30.0', '67.0', '97.0', '10.0', 'C23'], ['C22', 'cp', '40.0', '15.0', '40.0', '92.0', '122.0', '10.0', 'C24'], ['C23', 'cp', '38.0', '5.0', '30.0', '65.0', '95.0', '10.0', 'C21'], ['C24', 'cd', '38.0', '15.0', '-40.0', '148.0', '178.0', '10.0', 'C22'], ['C25', 'cp', '35.0', '5.0', '20.0', '154.0', '184.0', '0.0', 'C101'], ['C26', 'cd', '95.0', '30.0', '-10.0', '115.0', '145.0', '10.0', 'C28'], ['C27', 'cp', '95.0', '35.0', '20.0', '62.0', '92.0', '10.0', 'C91'], ['C28', 'cp', '92.0', '30.0', '10.0', '62.0', '92.0', '10.0', 'C26'], ['C29', 'cp', '90.0', '35.0', '10.0', '67.0', '97.0', '10.0', 'C93'], ['C30', 'cp', '88.0', '30.0', '10.0', '74.0', '104.0', '10.0', 'C32'], ['C31', 'cp', '88.0', '35.0', '20.0', '61.0', '91.0', '10.0', 'C89'], ['C32', 'cd', '87.0', '30.0', '-10.0', '131.0', '161.0', '10.0', 'C30'], ['C33', 'cp', '85.0', '25.0', '10.0', '51.0', '81.0', '10.0', 'C34'], ['C34', 'cd', '85.0', '35.0', '-10.0', '111.0', '141.0', '10.0', 'C33'], ['C35', 'cd', '67.0', '85.0', '-30.0', '139.0', '169.0', '10.0', 'C40'], ['C36', 'cd', '65.0', '85.0', '-8.0', '43.0', '73.0', '10.0', 'C72'], ['C37', 'cd', '65.0', '82.0', '-20.0', '124.0', '154.0', '10.0', 'C41'], ['C38', 'cp', '62.0', '80.0', '30.0', '75.0', '105.0', '10.0', 'C43'], ['C39', 'cp', '60.0', '80.0', '10.0', '37.0', '67.0', '10.0', 'C54'], ['C40', 'cp', '60.0', '85.0', '30.0', '85.0', '115.0', '10.0', 'C35'], ['C41', 'cp', '58.0', '75.0', '20.0', '92.0', '122.0', '10.0', 'C37'], ['C42', 'cp', '55.0', '80.0', '10.0', '33.0', '63.0', '10.0', 'C44'], ['C43', 'cd', '55.0', '85.0', '-30.0', '128.0', '158.0', '10.0', 'C38'], ['C44', 'cd', '55.0', '82.0', '-10.0', '64.0', '94.0', '10.0', 'C42'], ['C45', 'cp', '20.0', '82.0', '10.0', '37.0', '67.0', '10.0', 'C2'], ['C46', 'cd', '18.0', '80.0', '-20.0', '113.0', '143.0', '10.0', 'C12'], ['C47', 'cd', '2.0', '45.0', '-10.0', '45.0', '75.0', '10.0', 'C14'], ['C48', 'cd', '42.0', '5.0', '-14.0', '151.0', '181.0', '10.0', 'C83'], ['C49', 'cp', '42.0', '12.0', '10.0', '104.0', '134.0', '10.0', 'C20'], ['C50', 'cp', '72.0', '35.0', '30.0', '116.0', '146.0', '10.0', 'C80'], ['C51', 'cd', '55.0', '20.0', '-6.0', '83.0', '113.0', '10.0', 'C63'], ['C52', 'cp', '25.0', '30.0', '3.0', '52.0', '82.0', '10.0', 'C57'], ['C53', 'cp', '20.0', '50.0', '5.0', '91.0', '121.0', '10.0', 'C100'], ['C54', 'cd', '55.0', '60.0', '-10.0', '139.0', '169.0', '10.0', 'C39'], ['C55', 'cd', '30.0', '60.0', '-30.0', '140.0', '170.0', '10.0', 'C79'], ['C56', 'cd', '50.0', '35.0', '-6.0', '130.0', '160.0', '10.0', 'C90'], ['C57', 'cd', '30.0', '25.0', '-3.0', '96.0', '126.0', '10.0', 'C52'], ['C58', 'cd', '15.0', '10.0', '-16.0', '152.0', '182.0', '10.0', 'C75'], ['C59', 'cp', '10.0', '20.0', '19.0', '42.0', '72.0', '10.0', 'C97'], ['C60', 'cp', '15.0', '60.0', '17.0', '155.0', '185.0', '10.0', 'C70'], ['C61', 'cp', '45.0', '65.0', '9.0', '66.0', '96.0', '10.0', 'C68'], ['C62', 'cp', '65.0', '35.0', '3.0', '52.0', '82.0', '10.0', 'C94'], ['C63', 'cp', '65.0', '20.0', '6.0', '39.0', '69.0', '10.0', 'C51'], ['C64', 'cp', '45.0', '30.0', '17.0', '53.0', '83.0', '0.0', 'C103'], ['C65', 'cp', '35.0', '40.0', '16.0', '11.0', '41.0', '10.0', 'C74'], ['C66', 'cd', '41.0', '37.0', '-18.0', '133.0', '163.0', '10.0', 'C84'], ['C67', 'cp', '64.0', '42.0', '9.0', '70.0', '100.0', '10.0', 'C71'], ['C68', 'cd', '40.0', '60.0', '-9.0', '144.0', '174.0', '10.0', 'C61'], ['C69', 'cp', '31.0', '52.0', '27.0', '41.0', '71.0', '10.0', 'C78'], ['C70', 'cd', '35.0', '69.0', '-17.0', '180.0', '210.0', '10.0', 'C60'], ['C71', 'cd', '65.0', '55.0', '-9.0', '65.0', '95.0', '10.0', 'C67'], ['C72', 'cp', '63.0', '65.0', '8.0', '30.0', '60.0', '10.0', 'C36'], ['C73', 'cp', '2.0', '60.0', '5.0', '77.0', '107.0', '0.0', 'C106'], ['C74', 'cd', '20.0', '20.0', '-16.0', '141.0', '171.0', '10.0', 'C65'], ['C75', 'cp', '5.0', '5.0', '16.0', '74.0', '104.0', '10.0', 'C58'], ['C76', 'cp', '60.0', '12.0', '31.0', '75.0', '105.0', '0.0', 'C104'], ['C77', 'cd', '23.0', '3.0', '-13.0', '150.0', '180.0', '10.0', 'C87'], ['C78', 'cd', '8.0', '56.0', '-27.0', '90.0', '120.0', '10.0', 'C69'], ['C79', 'cp', '6.0', '68.0', '30.0', '89.0', '119.0', '10.0', 'C55'], ['C80', 'cd', '47.0', '47.0', '-30.0', '192.0', '222.0', '10.0', 'C50'], ['C81', 'cp', '49.0', '58.0', '10.0', '86.0', '116.0', '10.0', 'C96'], ['C82', 'cp', '27.0', '43.0', '9.0', '42.0', '72.0', '10.0', 'C16'], ['C83', 'cp', '37.0', '31.0', '14.0', '35.0', '65.0', '10.0', 'C48'], ['C84', 'cp', '57.0', '29.0', '18.0', '96.0', '126.0', '10.0', 'C66'], ['C85', 'cp', '63.0', '23.0', '2.0', '87.0', '117.0', '0.0', 'C102'], ['C86', 'cd', '21.0', '24.0', '-15.0', '87.0', '117.0', '10.0', 'C99'], ['C87', 'cp', '12.0', '24.0', '13.0', '90.0', '120.0', '10.0', 'C77'], ['C88', 'cd', '24.0', '58.0', '-9.0', '67.0', '97.0', '10.0', 'C98'], ['C89', 'cd', '67.0', '5.0', '-20.0', '144.0', '174.0', '10.0', 'C31'], ['C90', 'cp', '37.0', '47.0', '6.0', '86.0', '116.0', '10.0', 'C56'], ['C91', 'cd', '49.0', '42.0', '-20.0', '167.0', '197.0', '10.0', 'C27'], ['C92', 'cp', '53.0', '43.0', '14.0', '14.0', '44.0', '10.0', 'C95'], ['C93', 'cd', '61.0', '52.0', '-10.0', '178.0', '208.0', '10.0', 'C29'], ['C94', 'cd', '57.0', '48.0', '-3.0', '95.0', '125.0', '10.0', 'C62'], ['C95', 'cd', '56.0', '37.0', '-14.0', '34.0', '64.0', '10.0', 'C92'], ['C96', 'cd', '55.0', '54.0', '-10.0', '132.0', '162.0', '10.0', 'C81'], ['C97', 'cd', '4.0', '18.0', '-19.0', '120.0', '150.0', '10.0', 'C59'], ['C98', 'cp', '26.0', '52.0', '9.0', '46.0', '76.0', '10.0', 'C88'], ['C99', 'cp', '26.0', '35.0', '15.0', '77.0', '107.0', '10.0', 'C86'], ['C100', 'cd', '31.0', '67.0', '-5.0', '180.0', '210.0', '10.0', 'C53'], ['C101', 'cd', '35.0', '5.0', '-20.0', '154.0', '184.0', '10.0', 'C25'], ['C102', 'cd', '63.0', '23.0', '-2.0', '87.0', '117.0', '10.0', 'C85'], ['C103', 'cd', '45.0', '30.0', '-17.0', '53.0', '83.0', '10.0', 'C64'], ['C104', 'cd', '60.0', '12.0', '-31.0', '75.0', '105.0', '10.0', 'C76'], ['C105', 'cd', '25.0', '85.0', '-20.0', '145.0', '175.0', '10.0', 'C1'], ['C106', 'cd', '2.0', '60.0', '-5.0', '77.0', '107.0', '10.0', 'C73']]



# Max number of vehicles = number of pick ups
#max_vehicles = len(list(filter(lambda e: e[1] == "cp", data)))
max_vehicles = 8

# Monkey patching
Individual.get_fitness = get_fitness(data)

if __name__ == "__main__":

    for j in range(0, len(data)):
        for i in range(0,len(data)):
            if "S" in data[i][0]:
                data.pop(i)
                break
    if "S" in data:
        print("shoot")
    print(data[33])
    P = Population(size=20, optim="min", init_func=random_initialization(data, max_vehicles))
    # TODO change mut prob when mutation is implemented for our structure
    P.evolve(gens=100,
             xo_prob=1,
             mut_prob=0,
             select=tournament_sel,
             xo=vrp_single_point_xo(data),
             mutate=inversion_mutation,
             elitism=True)

import turtle
import mesa
import random
import tkinter.messagebox

from utils.calcula_disntacia import distance
from utils.nomes import nomes


ID = 4
RANGE = 5
TAMANHO_MAPA = 200
COORD_INICIO = (-170, 180)
COORD_CIVIL = (150, -180)
COOR_CENTER = (0, 0)


window = tkinter.Tk()
canvas = tkinter.Canvas(master=window, width=400, height=400)
canvas.grid(padx=2, pady=2, row=0, column=0, rowspan=10, columnspan=10)
screen = turtle.TurtleScreen(canvas)



class Pessoa(mesa.Agent):
    def __init__(self, unique_id, model, x, y):
        super().__init__(unique_id, model)
        self.x = x
        self.y = y
        self.nome = nomes[unique_id]
        self.energiaHeroi = random.randint(200, 350)
        self.resgatados = 0
        self.vontade = 0
        self.centro = random.randint(0, 2)
        self.escondido = False
        self.isRescued = False
        self.shape = turtle.RawTurtle(screen)
        self.shape.hideturtle()
 
        self.shape.penup()
        self.shape.setposition(self.x, self.y)
        self.shape.showturtle()

    def move(self):
        if(self.isRescued == True):
            self.resgatados += 1
        if(self.centro != 0):
            if(self.isRescued == True and self.resgatados < 2): #pegando um civil de cada vez
                self.backtoinitialpoint()
            else:
                self.gotocenter()
        elif(self.energiaHeroi == 0): #nessa condição, a gente podia pensar em uma forma de interação. Se o herói morrer, o civil tenta fugir ou morre também ?
            self.walk_monster() #SÓ PARA TESTAR O A FORMA ALEATÓRIA DE ANDAR
        elif(distance(self.shape.position(), COORD_CIVIL) < 380 and self.isRescued == False and self.vontade == 1):
            self.gotocivil()
        else:
            if self.shape.xcor() >= 180:
                self.x -= 5
            elif self.shape.ycor() >= 180:
                self.y -= 5
            elif self.shape.xcor() <= -180:
                self.x += 5
            elif self.shape.ycor() <= -180:
                self.y += 5
            else:
                self.x += random.randint(-5, 5)
                self.y += random.randint(-5, 5)

            self.shape.goto(self.x, self.y)

            self.vontade = random.randint(1, 50)

            self.energiaHeroi -= 1


    def backtoinitialpoint(self):
        x, y = self.shape.position()
        xs, ys = COORD_INICIO

        if x > xs:
            self.x -= 5
        if y < ys:
            self.y += 5

        if x <= 0 and y >= 0: #REVER ISSO AQUI
            self.centro = 0

        self.shape.goto(self.x, self.y)

    def gotocenter(self):
        x, y = self.shape.position()
        xs, ys = COOR_CENTER

        if x < xs:
            self.x += 5
        if y > ys:
            self.y -= 5

        if x >= 0 and y <= 0:            self.centro = 0

        self.shape.goto(self.x, self.y)

    def gotocivil(self):
        x, y = self.shape.position()
        xs, ys = COORD_CIVIL

        if x < xs:
            self.x += 5
        if y > ys:
            self.y -= 5

        if(x >= 150 and y <= -180):
            self.energiaHeroi += random.randint(1, 10)
            self.isRescued = True
 
            escreverLog(f'heroi salvou {self.nome}')
            self.centro = random.randint(0, 3)

        self.shape.goto(self.x, self.y)

    def gotosaida(self):
        x, y = self.shape.position()
        xs, ys = COORD_INICIO

        if x < xs:
            self.x += 5
        if y < ys:
            self.y += 5

        if(x >= 160 and y >= 180):
            self.shape.hideturtle()
            if(not self.escondido):
                escreverLog(f'{self.nome} saiu da balada')
                self.escondido = True


        self.shape.goto(self.x, self.y)

    def mostra_status(self):
        print(self.nome + " tem " + str(self.energiaHeroi) + " sobrando")
    
    def walk_monster(self):
        # Lógica para andar aleatoriamente pelo mapa
        dx = random.randint(-10, 10)
        dy = random.randint(-30, 30)
        
        # Adicionando um fator de aleatoriedade para a direção dos movimentos
        dx *= random.choice([-1, 1])
        dy *= random.choice([-1, 1])

        self.x += dx
        self.y += dy

        # Limitando as coordenadas para que o boneco permaneça dentro dos limites do mapa
        self.x = max(min(self.x, 180), -180)
        self.y = max(min(self.y, 180), -180)
        
 
        self.shape.goto(self.x, self.y)
    


class GameModel(mesa.Model):
    def __init__(self, N):
        self.num_monstros = N
        self.schedule = mesa.time.SimultaneousActivation(self)
        self.pessoas = []
        self.id = 10

        for i in range(self.num_monstros):
            p = Pessoa(i, self, -170, 180)
            self.pessoas.append(p)
            self.schedule.add(p)
            escreverLog(f'{p.nome} entrou na balada')

    def step(self):
        for pessoa in self.schedule.agents:
            pessoa.move()
            if(pessoa.energiaHeroi == 0 ):
                self.schedule.remove(pessoa)
                #escreverLog(f'{self.nome}, heroi, foi morto')

    def numero_pessoas(self):
        print(self.schedule.get_agent_count())

    def remover_pessoa(self):
        for i in self.pessoas:
            i.mostra_status()

    def adicionar_pessoa(self):
        a = Pessoa(self.id, self, -170, 180)
        self.id += 1
        self.pessoas.append(a)
        self.schedule.add(a)

    def next_agent_id(self):
        return max([agent.unique_id for agent in self.schedule.agents]) + 1


def escreverLog(mensagem):
    log = open("utils/log.txt", "a")
    log.write(f"{mensagem}\n")
    log.close()


FLAG = True

# Test Tkinker
global game
game = GameModel(10)


def Play():
##    mixer.music.play()
    while FLAG:
        game.step()


def funcao_placeholder():
    game.remover_pessoa()


def adicionar_herois():
    game.adicionar_heroi()


Play_Button = tkinter.Button(
    master=window, text="Iniciar simulação", command=Play)
Play_Button.config(bg="light gray", fg="black")
Play_Button.grid(padx=2, pady=2, row=0, column=11, sticky='nsew')

Board_Button = tkinter.Button(
    master=window, text="Check todo mundo", command=funcao_placeholder)
Play_Button.config(bg="light gray", fg="black")
Board_Button.grid(padx=2, pady=2, row=1, column=11, sticky='nsew')

Board_Button = tkinter.Button(
    master=window, text="Adicionar Heróis", command=adicionar_herois)
Play_Button.config(bg="light gray", fg="black")
Board_Button.grid(padx=2, pady=2, row=2, column=11, sticky='nsew')
window.mainloop()
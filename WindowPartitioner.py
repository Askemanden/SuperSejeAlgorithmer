import pygame
import json

def intet():
    pass



# INFO-Klasser

class UI_info():                                                        # Basisklasse for alle info og udvidelsesklasser til et komponent.
    def __init__ (self):
        pass
    def update(self):
        pass
    def event_handling(self, event):
        pass
    def draw(self, screen):
        pass


class UI_component_placement_info(UI_info):
    def __init__(self, x, y, width, height, anchor_x = "left", anchor_y = "top"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.anchor_x = anchor_x
        self.anchor_y = anchor_y

class UI_component_color_info(UI_info):
    def __init__(self, primary_color = (100, 149, 237), secondary_color = (0, 70, 148), accent_color = (227, 209, 120)):
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.accent_color = accent_color
        self.primary_complementary_color = (255 - primary_color[0], 255 - primary_color[1], 255 - primary_color[2])
        self.secondary_complementary_color = (255 - secondary_color[0], 255 - secondary_color[1], 255 - secondary_color[2])

# UDVIDELSES-Klasser

class UI_component_text(UI_info):
    def __init__(self, component, text = "Hej verden", size = 20):
        self.component = component
        
        self.text = text
        self.size = size
        self.font = pygame.font.SysFont('yu_gothic', self.size)
        self.bold_font = pygame.font.SysFont('yu_gothic', self.size, bold=True)
        self.bold = False

    def get_text_color(self):
        if isinstance(self.component.color_info, UI_component_color_info):
            return self.component.color_info.primary_complementary_color
        else:
            return self.component.parent_box.color_info.secondary_complementary_color

    def update(self):
        if self.component.hovered:
            self.bold = True
        else:
            self.bold = False

    def draw(self, screen):
        image = self.font.render(self.text, True, self.get_text_color())
        self.text_rect = image.get_rect()
 
        if self.bold:
            text_surface = self.bold_font.render(self.text, True, self.get_text_color(), None)
        else:
            text_surface = self.font.render(self.text, True, self.get_text_color(), None)
        screen.blit(text_surface, (self.component.rect.x  + (0.5 * (self.component.rect.width - self.text_rect.width)), self.component.rect.y + self.component.rect.height * 0.2))


class UI_button_extension(UI_info):
    def __init__(self, component, function = intet):
        self.function = function
        self.component = component

    def event_handling(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.component.rect.collidepoint(event.pos):
                self.function()

    def update(self):
        if self.component.rect.collidepoint(pygame.mouse.get_pos()):   
            self.component.hovered = True
        else:
            self.component.hovered = False

# UI-Komponenter

class UI_component:                                         # Basisklasse for alle UI komponenter til et UI_element.
    def __init__(self, visible = True, placement_info: UI_component_placement_info = UI_info(), color_info: UI_component_color_info = UI_info()):
        self.color_info = color_info
        self.hovered = False
        self.placement_info = placement_info
        self.text = UI_info()
        self.button = UI_info()
        self.parent_box = None
        self.rect = pygame.Rect(0, 0, 10, 10)
        self.drawing_method = None
        if visible:
            self.drawing_method = self.drawing_helper_visible
        else:
            self.drawing_method = self.drawing_helper_invisible

    def update_color(self):
        if not isinstance(self.color_info, UI_component_color_info):
            self.color_info = self.parent_box.color_info

    def update(self):
        self.color_info.update()
        self.placement_info.update()
        self.text.update()
        self.button.update()

    def event_handling(self, event):
        self.button.event_handling(event)

    def draw_visible(self, screen):
        if not isinstance(self.color_info, UI_component_color_info):
           color_source = self.parent_box.color_info.secondary_color
           accent_color = self.parent_box.color_info.accent_color
        else:
            color_source = self.color_info.primary_color
            accent_color = self.color_info.accent_color
        
        #pygame.draw.rect(screen, (100, 100, 100), self.rect)
        if self.hovered:
            #brighter_color = (min(color_source.secondary_color[0] + 40, 255), min(color_source.secondary_color[1] + 40, 255), min(color_source.secondary_color[2] + 40, 255))
            brighter_color = accent_color
            pygame.draw.rect(screen, brighter_color, self.rect)
        else:
            pygame.draw.rect(screen, color_source, self.rect)
        self.text.draw(screen)

    def draw_invisible(self, screen):
        self.text.draw(screen)

    def drawing_helper_invisible(self):
        self.draw_invisible(self.screen)

    def drawing_helper_visible(self):
        self.draw_visible(self.screen)

    def draw(self, screen):
       self.screen = screen
       self.drawing_method()

# UI-Element

class UI_element:                                                       # Basisklasse for alle UI elementer.
    def __init__(self, placement : UI_component_placement_info):
        self.screen_position_x = placement.x - placement.width * 0.5
        self.screen_position_y = placement.y - placement.height * 0.5
        self.rect = pygame.Rect(self.screen_position_x, self.screen_position_y, placement.width, placement.height)                           # Basisklasse har en rektangel.
        self.color_info = UI_info()

    def update(self):
        pass

    def move(self, x : int, y : int):
        pass

    def draw(self, screen : pygame.Surface):
        pass

class screen_box (UI_element):                                       # En boks på skærmen der kan indeholde knapper og items.
    def __init__(self, placement : UI_component_placement_info, color : UI_component_color_info, border_width = 8):
        super().__init__(placement)
        #self.screen_position_x = placement.x - placement.width * 0.5
        #self.screen_position_y = placement.y - placement.height * 0.5
        #self.rect = pygame.Rect(self.screen_position_x, self.screen_position_y, placement.width, placement.height)

        self.border_width = border_width
        
        self.color_info = color
        self.fill_color = (198, 198, 198)
        self.border_color = color.primary_color
       
        self.components = []
        self.number_of_buttons = 0                                      # Antallet af automatisk placerede knapper i listen af containere. Bruges til at arrangere knapperne jævnt.

    def create_UIcomponent(self, visible = True, color : UI_component_color_info = UI_info(), placement_info : UI_component_placement_info = UI_info(), text = "", text_size = 20, function = None):
        component = UI_component(visible, placement_info, color)
        component.parent_box = self
        text_object = UI_component_text(component, text, text_size)
        component.text = text_object
        if function != None:
            button_object = UI_button_extension(component, function)
            component.button = button_object

        self.components.append(component)
        self.place_all_components()
    
    def count_buttons(self):                                            # Tæller antallet af automatisk placerede knapper i listen af containere.
        count = 0
        for container in self.components:
            if not isinstance(container.placement_info, UI_component_placement_info) and isinstance(container.button, UI_button_extension):
                count += 1
        self.number_of_buttons = count

    def remove_container(self, container):                              # Fjerner en container fra listen af containere.
        pass # TODO

    def update(self):                                                   # Opdaterer tilstanden af screen_boxen og dens containere.
                                                                        # update kalder ikke den matematiktunge place_all_buttons, da den kun behøver at blive kaldt når en container tilføjes eller fjernes, eller kassen flyttes.
        for container in self.components:
           container.update()
        #for event in pygame.event.get():
        #    for component in self.components:
        #        component.event_handling(event)

    def place_component(self, component, automatic_button_index):       # sætter x og y positionen for en knap baseret på dens placering KUN i forhold til andre af dens type.
                                                                        # Bredden og højden beregnes af screen_boxen, da dette er lettere.
        if isinstance(component.placement_info, UI_component_placement_info):   # Component er en knap med manuel layout info.

            if component.placement_info.anchor_x == "center":
                component.rect.x = self.rect.x + (self.rect.width - component.placement_info.width) * 0.5 + component.placement_info.x
            else:
                component.rect.x = self.rect.x + component.placement_info.x

            if component.placement_info.anchor_y == "center":
                component.rect.y = self.rect.y + (self.rect.height - component.placement_info.height) * 0.5 + component.placement_info.y
            else:
                component.rect.y = self.rect.y + component.placement_info.y

        else:
            if isinstance(component.button, UI_button_extension):
                button_height = component.rect.height
                button_width = component.rect.width
                component.rect.x = self.rect.x + self.border_width + automatic_button_index * (button_width + self.border_width)
                component.rect.y = self.rect.y + self.rect.height - self.border_width - button_height

            elif isinstance(component, label):
                component.rect.x = self.rect.x + self.border_width
                component.rect.y = self.rect.y + self.border_width
                component.rect.width = self.rect.width - self.border_width * 2
                component.rect.height = self.rect.height - (self.border_width * 2 + 40 * 1.2) # 40 er standarden for knaphøjde. TODO: Gør dette dynamisk baseret på screen_boxens højde.
    
    def place_all_components(self):
        self.count_buttons()
        automatic_button_index = 0

        for container in self.components:

            if not isinstance(container.placement_info, UI_component_placement_info):
                if isinstance(container.button, UI_button_extension):    # Automatisk placeret knap.
                    container.rect.width = (self.rect.width - self.border_width * (self.number_of_buttons + 1)) / self.number_of_buttons
                    container.rect.height = 40 # Standard højde for knapper. TODO: Gør dette dynamisk baseret på screen_boxens højde.
                    automatic_button_index += 1
                else:
                    pass
                    # Det er ikke en automatisk placeret knap.
                    #TODO implementer håndtering af komponenter uden placement_info der ikke er en knap
            else:
                container.rect.width = container.placement_info.width
                container.rect.height = container.placement_info.height

            self.place_component(container, automatic_button_index - 1)  # -1 fordi indexet er blevet forøget efter placeringen af knappen.
                
    def move(self, x, y):
        self.screen_position_x = x - self.rect.width * 0.5
        self.screen_position_y = y - self.rect.height * 0.5
        self.rect.topleft = (self.screen_position_x, self.screen_position_y)
        self.place_all_components()

    def event_handler(self, event):
        for component in self.components:
            component.event_handling(event)

    def draw(self, screen):
        # Tegner en boks med en kant. Kanten er border_width pixels bred.
        border_rect = pygame.Rect(self.rect.left - self.border_width, self.rect.top - self.border_width, self.rect.width + self.border_width * 2, self.rect.height + self.border_width * 2)
        pygame.draw.rect(screen, self.border_color, border_rect)
        pygame.draw.rect(screen, self.fill_color, self.rect)

        # Tegner alle UI-komponenter i boksen.
        # For nu arrangeres alle knapper, vandret i bunden af boksen. Lidt ligesom Windows pop-up menuer.
        # Alle andre UI-komponenter arrangeres lodret i toppen af boksen, og der kan scrolles gennem dem.
        for container in self.components:
            container.draw(screen)


class dropdown(screen_box):
    def __init__(self, placement : UI_component_placement_info, color : UI_component_color_info):
        super().__init__(placement, color)
        self.placement_info = placement
        self.color_info = color

# JSON

main_menu =  {
    "0": {
        "color_info": [ 160, 160, 160, 120, 160, 180, 134, 189, 0 ],
        "placement_info": [ 400, 200, 600, 300, "center", "center" ],
        "components": [
            {
            "color_info": None,
            "visible": True,
            "placement_info": None,
            "text": "Afslut",
            "text_size": None,
            "button_function": "quit"
        },
            {
            "color_info": None,
            "visible": True,
            "placement_info": None,
            "text": "Spil",
            "text_size": None,
            "button_function": "start"
        },
            {
            "color_info": [ 255, 255, 255, 43, 80, 170, 79, 168, 111 ],
            "visible": True,
            "placement_info": [ 0, 20, 140, 0, "center", "Askeslaske" ],
            "text": "Das Spiel",
            "text_size": 60,
            "button_function": None
        },
            {
            "color_info": None,
            "visible": True,
            "placement_info": [ 0, 100, 140, 0, "center", "Askeslaske" ],
            "text": "Das spiel, der Übermenschen",
            "text_size": 26,
            "button_function": None
        },
            {
            "color_info": None,
            "visible": True,
            "placement_info": [ 0, 130, 140, 0, "center", "Askeslaske" ],
            "text": "Skabt af Jacob, Aske og Louis",
            "text_size": 15,
            "button_function": None
        }
        ]
    },
    "1": {
        "color_info": [ 160, 160, 160, 120, 160, 180, 134, 189, 0 ],
        "placement_info": [ 400, 200, 600, 300, "center", "center" ],
        "components": [
                {
                "color_info": None,
                "visible": True,
                "placement_info": None,
                "text": "knap0",
                "text_size": None,
                "button_function": "quit"
            }
        ]
    }
}

 
#with open("menu.json", "w", encoding="utf-8") as f:
#    json = json.dump(main_menu, f, indent=4)



function_map = {
    "quit": quit,
    "start": start,
    None: None
}

menus = []

def create_menu_from_json(json_data : dict, menu_index : int, local_function_map) -> screen_box:
    json_data = json_data[f"{menu_index}-screen_box"]
    placement_info = UI_component_placement_info(
        json_data["placement_info"][0],
        json_data["placement_info"][1],
        json_data["placement_info"][2],
        json_data["placement_info"][3],
        json_data["placement_info"][4],
        json_data["placement_info"][5]
        )
    color_info = UI_component_color_info(
        (json_data["color_info"][0], json_data["color_info"][1], json_data["color_info"][2]),
        (json_data["color_info"][3], json_data["color_info"][4], json_data["color_info"][5]),
        (json_data["color_info"][6], json_data["color_info"][7], json_data["color_info"][8])
    )
    if "border" in json_data:
        border = json_data["border"]
    else:
        border = 8

    menu = screen_box(placement_info, color_info, border)

    for index in range(len(json_data["components"])):
        

        index_component = json_data["components"]
        component_color = UI_info()
        component_placement = UI_info()
        component_text = None
        component_text_size = 20

        if  index_component["color_info"] != None:
            component_color = UI_component_color_info(
                (index_component["color_info"][0], index_component["color_info"][1], index_component["color_info"][2]),
                (index_component["color_info"][3], index_component["color_info"][4], index_component["color_info"][5]),
                (index_component["color_info"][6], index_component["color_info"][7], index_component["color_info"][8])
            )
        if index_component["placement_info"] != None:
            component_placement = UI_component_placement_info(
                index_component["placement_info"][0],
                index_component["placement_info"][1],
                index_component["placement_info"][2],
                index_component["placement_info"][3],
                index_component["placement_info"][4],
                index_component["placement_info"][5]
            )
        if index_component["text"] != None:
                component_text = index_component["text"]

        if index_component["text_size"] != None:
            component_text_size = int(index_component["text_size"])

        if index_component["button_function"] != None:
            func_key = index_component["button_function"]
            func_key = local_function_map.get(func_key, None)
        else:
            func_key = None

        menu.create_UIcomponent(index_component["visible"], component_color, component_placement, component_text, component_text_size, func_key)
    #menus.append(menu)
    return menu

def create_json_from_menu(output : str, menu : screen_box) -> dict:
    
    menu_dict = {
        "color_info" : [ 160, 160, 160, 120, 160, 180, 134, 189, 0 ],
        "placement_info" : [ 400, 200, 600, 300, "center", "center" ],
        "components" : []
    }

    
    

    try:
        with open(output, "w", encoding="utf-8") as f:
            json = json.dump(menu_dict, f, indent=4)
            return json
    except:
        print("Mongol")
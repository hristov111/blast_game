def make_List():
    list = []
    def vertically_left(x,y):
        while y!=0:
            list.append((x,y))
            y-=100
        horizontally_up_left(x,y)
    def horizontally_up_left(x,y):
        while x!=800:
            list.append((x, y))
            x+=100
        vertically_right(x,y)
    def vertically_right(x,y):
        while y!=600:
            list.append((x, y))
            y+=100
        horizontally_down_right(x,y)
    def horizontally_down_right(x,y):
        while x!=320:
            list.append((x, y))
            x-=160
    def horizontally_down_left(x,y):
        while x!= 0:
            list.append((x, y))
            x-=160
        vertically_left(x,y)
    horizontally_down_left(320,600)
    return list



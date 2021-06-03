from numpy import array,sin,cos,pi,dot
from copy import copy
from numpy.linalg import norm

scale=8

class bird:
    def __init__(self,p,max_v,prameters,n=""):
        size=sum(prameters)
        self.prameters=[q/size for q in prameters]

        self.p=array(p)
        self.max_v=max_v
        self.pL=[]
        self.pL.append([self.p[0],self.p[1]])
        self.v=array([1,0])
        self.next_p=copy(self.p)
        self.next_v=copy(self.v)

        self.name=n

        self.ydata=[]

    def follow(self,t):
        return(array([1,0]))
        if t<20:
            return(array([1,0]))
        if t<40:
            return(array([cos((t-20)*pi/40),sin((t-20)*pi/40)]))
        else:
            return(array([0,1]))
            
    def dist2(self,b):return((self.p[0]-b.p[0])**2+(self.p[1]-b.p[1])**2)
    
    def in_dist(self,boidL,r):
        L=[]
        r2=r**2
        for b in boidL:
            if 0<self.dist2(b)<r2:
                L.append(b)
        return(L)
    
    def Separation(self,bL):
        bL=self.in_dist(bL,3)
        if bL==[]:return(array([0,0]))
        else:
            c=0
            p=array([0,0])
            for b in bL:
                
                c+=1
                p=p+b.p

            
            p=p/c
            size=norm([p[0]-self.p[0],p[1]-self.p[1]])
            if size==0:
                x=0
                y=0
            else:
                x=(self.p[0]-p[0])/size
                y=(self.p[1]-p[1])/size
            return(array([x,y]))

    def escape(self,bL):
        c=0
        p=array([0,0])
        r2=36#6^2
        for b in bL:
            if b.name=="eagle":
                if 0<self.dist2(b)<r2:
                    c+=1
                    p=p+b.p
        if c>0:
            p=p/c
            size=norm([p[0]-self.p[0],p[1]-self.p[1]])
            x=(self.p[0]-p[0])/size
            y=(self.p[1]-p[1])/size
            return(array([x,y]))
        else:
            return([0,0])

    def cohesion_alignment(self,bL):

        if len(bL)<2:
            return([self.p,[0,0]])
        
        else:
            sbL=sorted(bL,key=self.dist2)
            if len(sbL)>7:sbL=sbL[:6]

            p=array([0.0,0.0])
            v=array([0.0,0.0])
            for b in sbL:

                p=p+b.p
                v=v+b.v

            size=norm([p[0]-self.p[0],p[1]-self.p[1]])
            if size==0:
                x=0
                y=0
            else:
                x=(p[0]-self.p[0])/size
                y=(p[1]-self.p[1])/size

            v=v/norm(v)

            return(array([x,y]),v)
    
    def np(self,bL,dt,t):

        x=self.cohesion_alignment(bL)
        forces=[x[0],x[1],self.Separation(bL),self.follow(t),self.escape(bL)]
        
        
        self.next_v=dot(self.prameters,forces)
        
        self.next_v=self.max_v*self.next_v#/norm(self.next_v)
        self.next_p=self.p+array(self.v)*dt
        self.pL.append(copy(self.next_p))
        self.v=self.next_v
        self.p=self.next_p

class eagle:
    chatch_range=1
    def __init__(self,p,max_v,prameters,n="eagle"):
        size=sum(prameters)
        self.prameters=self.prameters=[q/size for q in prameters]
        
        self.hanger=1#timer until the start of new hunt

        self.p=array(p)
        self.max_v=max_v
        self.pL=[]
        self.pL.append([self.p[0],self.p[1]])
        self.v=array([1,0])
        self.next_p=copy(self.p)
        self.next_v=copy(self.v)
        self.name=n
        self.f_list=[]

    def fly(self,t):
        return(array([0,1]))

    def dist2(self,b):return((self.p[0]-b.p[0])**2+(self.p[1]-b.p[1])**2)
    
    def in_dist(self,boidL,r):
        L=[]
        r2=r**2
        for b in boidL:
            if 0<self.dist2(b)<r2:
                L.append(b)
        return(L)
    
    def separation(self,bL):
        bL=self.in_dist(bL,3)
        if bL==[]:return(array([0,0]))
        else:
            c=0
            p=array([0,0])
            for b in bL:
                if self.name!="":
                
                    c+=1
                    p=p+b.p

            
            p=p/c
            size=norm([p[0]-self.p[0],p[1]-self.p[1]])
            if size==0:
                x=0
                y=0
            else:
                x=(p[0]-self.p[0])/size
                y=(p[1]-self.p[1])/size
            
            return(-array([x,y]))

    def hunt(self,bL):
        if self.hanger > 0:
            return([0,0])
        else:
            #find the closest target
            target=bL[1]

            for b in bL:

                if b.name!=self.name:

                    if self.dist2(target)>self.dist2(b):
                        target=copy(b)


            size = norm([target.p[0] - self.p[0], target.p[1] - self.p[1]])
            if size<eagle.chatch_range and self.hanger<0:
                target.p[1]+=10000
                self.hanger=10000
                return(array([0,0]))
            x=(target.p[0]-self.p[0])/size
            y=(target.p[1]-self.p[1])/size


            return(array([x,y]))
    
    def np(self,bL,dt,t):
        global scale
        hunting=self.hunt(bL)
        fly=self.fly(t)
        if self.hanger>0:
            hunting=array([0,0])
        else:
            pass
            fly=array([0,0])
        self.hanger -= dt

        forces=[hunting,self.separation(bL),fly]
        
        self.next_v=dot(self.prameters,forces)
        size=max([norm( [self.prameters[i]* forces[i][0],self.prameters[i]* forces[i][1]])
                 for i in range(len(self.prameters))])


        self.f_list.append([[self.p[0] + self.prameters[i]  * scale * forces[i][0] / size,
                               self.p[1] + self.prameters[i]  * scale * forces[i][1] / size]
                             for i in range(len(self.prameters))])#for drowing the forces

        self.next_v=self.max_v*self.next_v#/norm(self.next_v)
        self.next_p=self.p+array(self.v)*dt
        self.pL.append(copy(self.next_p))
        self.v=self.next_v
        self.p=self.next_p

# Streamlitライブラリをインポート
import streamlit as st
kannsuu=7

# ページ設定（タブに表示されるタイトル、表示幅）
st.set_page_config(page_title="タイトル", layout="wide")

# タイトルを設定
st.title('楕円曲線')
#daenn 

class EllipticCurve():
    def __init__(self, a, b, c, d):
        if a == 0:
            raise ValueError("a=0 is forbidden!")
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def isin(self, p):
        if p == 0:
            return True
        x, y = p[0], p[1]
        value = y**2 - self.a * (x ** 3) - self.b * (x**2) - self.c * x - self.d
        if value == 0:
            return True
        return False

    def sum(self, p, q):
        if not self.isin(p):
            raise ValueError("{} is not in the elliptic curve".format(p))
        if not self.isin(q):
            raise ValueError("{} is not in the elliptic curve".format(q))

        if p == 0:
            return q
        if q == 0:
            return p
        x1, y1 = p[0], p[1]
        x2, y2 = q[0], q[1]

        if x1 != x2:
            x3 = (1 / self.a) * ((y2-y1) / (x2-x1)) ** 2 - (self.b / self.a) - x1 - x2
            y3 = ((y2-y1) / (x2-x1)) * -x3 + ((y2*x1 - y1*x2) / (x2 - x1))
            return (x3, y3)

        if x1 == x2 and y1 == -1 * y2:
            return 0

        if x1 == x2 and y1 != -1 * y2:
            x3 = ((1 / (4 * self.a * y1 ** 2))) *\
                 (self.a ** 2  * x1 **4 - 2 * self.a * self.c * x1 ** 2\
                    - 8* self.a * self.d * x1 - 4 * self.b * self.d)
            y3 = (1 / (8 * self.a * y1 ** 3)) *\
                 (self.a ** 3 * x1 ** 6 + 2 * self.a **2  * self.b * x1 ** 5\
                    + 5 * self.a**2 * self.c * x1 ** 4  + 20 * self.a ** 2 * self.d * x1 ** 3\
                    + (20 * self.a * self.b * self.d - 5 * self.a * self.c **2) * x1**2\
                    + (8 * self.b**2 * self.d - 2 * self.b * self.c**2 - 4 * self.a * self.c * self.d) * x1\
                    + (4 * self.b * self.c * self.d - 8 * self.a * self.d**2  - self.c**3)
                 )
            return (x3, y3)
        
class EllipticCurveModPrimeNum():
    def __init__(self, a, b, c, d, prime_number):
        if a == 0:
            raise ValueError("a=0 is forbidden!")
        
        self.a = a % prime_number
        self.b = b % prime_number
        self.c = c % prime_number
        self.d = d % prime_number
        self.p = prime_number

    def isin(self, pt):
        if pt == 0:
            return True

        x, y = pt[0] % self.p , pt[1] % self.p
        value = y**2 - self.a * (x ** 3) - self.b * (x**2) - self.c * x - self.d

        if value % self.p == 0:
            return True
        return False

    def sum(self, pt_1, pt_2):
        if not self.isin(pt_1):
            raise ValueError("{} is not in the elliptic curve".format(pt_1))
        if not self.isin(pt_2):
            raise ValueError("{} is not in the elliptic curve".format(pt_2))

        if pt_1 == 0:
            return pt_2
        if pt_2 == 0:
            return pt_1

        x1, y1 = pt_1[0] % self.p, pt_1[1] % self.p
        x2, y2 = pt_2[0] % self.p, pt_2[1] % self.p

        if x1 != x2:
            x3 = ((self.a ** (self.p - 2) * (y2-y1) ** 2 * (x2-x1) ** (2 * self.p - 4) ) % self.p \
                    - (self.b * self.a ** (self.p - 2)) % self.p\
                    - x1 - x2
                ) % self.p
            y3 = ((-1 * (y2-y1) * (x2-x1) ** (self.p - 2) * x3 ) % self.p \
                + (y2*x1 - y1*x2) * (x2 - x1) ** (self.p - 2) % self.p
                ) % self.p
            return (x3, y3)

        if x1 == x2 and y1 == -1 * y2 % self.p :
            return 0

        if x1 == x2 and y1 != -1 * y2 % self.p:
            x3 = ((4 * self.a * y1 ** 2  % self.p) ** (self.p - 2) % self.p  *\
                  (self.a ** 2  * x1 ** 4 \
                    - 2 * self.a * self.c * x1 ** 2 % self.p\
                    - 8 * self.a * self.d * x1 % self.p
                    - 4 * self.b * self.d % self.p)
            ) % self.p
            y3 = ((8 * self.a * y1 ** 3 % self.p) ** (self.p - 2) % self.p *\
                  (self.a ** 3 * x1 ** 6 % self.p \
                    + 2 * self.a ** 2  * self.b * x1 ** 5 % self.p\
                    + 5 * self.a ** 2 * self.c * x1 ** 4 % self.p \
                    + 20 * self.a ** 2 * self.d * x1 ** 3 % self.p\
                    + (20 * self.a * self.b * self.d % self.p - 5 * self.a * self.c ** 2 % self.p) % self.p * ((x1 ** 2) % self.p) % self.p\
                    + (8 * self.b ** 2 * self.d % self.p - 2 * self.b * self.c ** 2 % self.p - 4 * self.a * self.c * self.d % self.p) * (x1 % self.p) % self.p \
                    + (4 * self.b * self.c * self.d % self.p - 8 * self.a * self.d ** 2 % self.p  - self.c ** 3 % self.p) % self.p )
            ) % self.p

            return (x3, y3)

weight1 = st.number_input("aを入力してください", min_value=-100)
weight2 = st.number_input("bを入力してください", min_value=-100)
weight3 = st.number_input("cを入力してください", min_value=-100)
weight4 = st.number_input("dを入力してください", min_value=-100)        
win = st.number_input("素数", min_value=2)  
st.write('y^2=ax^3+bx^2+cx+d')
weight = st.number_input("xを入力してください", min_value=-100)
st.write(weight1*weight*weight*weight+weight2*weight*weight+weight3*weight*weight4)
weighta = st.number_input("yを入力しください", min_value=-100)      
st.write(weighta*weighta)
weightb = st.number_input("Xを入力ください", min_value=-100)
st.write(weight1*weightb*weightb*weightb+weight2*weightb*weightb+weight3*weightb*weight4)
weightac = st.number_input("Yを入ください", min_value=-100)      
st.write(weightac*weightac)
pt1 = (weight,weighta)
pt2=(weightb,weightac)



if st.button("mod"):
    
    st.write(win)    
    kannsuu=win
    ell = EllipticCurveModPrimeNum(1,0,0,1,win)
    st.write(ell.sum(pt1,pt2))

if st.button("modなし"):
    
    st.write(win)    
    kannsuu=win
    ell = EllipticCurve(weight1,weight2,weight3,weight4)
    st.write(ell.sum(pt1,pt2))
      
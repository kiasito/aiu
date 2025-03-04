# Streamlitライブラリをインポート
import streamlit as st
kannsuu=7

# ページ設定（タブに表示されるタイトル、表示幅）
st.set_page_config(page_title="タイトル", layout="wide")

# タイトルを設定
st.title('楕円曲線')
#daenn
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
        
win = st.number_input("素数", min_value=2)  
st.write('y^2=x^3+1割る素数')
weight = st.number_input("xを入力してください", min_value=0)
st.write(weight*weight*weight+1)
weighta = st.number_input("yを入力しください", min_value=0)      
st.write(weighta*weighta)
weightb = st.number_input("Xを入力ください", min_value=0)
st.write(weight*weight*weight+1)
weightac = st.number_input("Yを入ください", min_value=0)      
st.write(weighta*weighta)
pt1 = (weight,weighta)
pt2=(weightb,weightac)


if st.button("クリック"):
    
    st.write(win)    
    kannsuu=win
    ell = EllipticCurveModPrimeNum(1,0,0,1,win)
    st.write(ell.sum(pt1,pt2))
   
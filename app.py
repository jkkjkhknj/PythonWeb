# 导入所需的库
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

plt.rcParams['font.sans-serif'] = ['SimHei'] #显示中文标签
plt.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题


# 读取csv文件
df1 = pd.read_csv('各省的订单数量.csv',encoding='gbk')
df2 = pd.read_csv('年龄段分析.csv',encoding='gbk')
df3 = pd.read_csv('用户行为分析.csv',encoding='gbk')
df4 = pd.read_csv('前十商品.csv',encoding='gbk')
df5 = pd.read_csv('性别.csv',encoding='gbk')
df6 = pd.read_csv('用户评分.csv',encoding='gbk')

# 绘制各省订单数量排行前十的柱形图
df1 = df1.sort_values(by='数量', ascending=False) # 按数量降序排列
df1_top10 = df1.head(10) # 取前十行
plt.figure(figsize=(10, 6)) # 设置画布大小
plt.bar(df1_top10['省份'], df1_top10['数量'], color='green') # 绘制柱形图
plt.xlabel('省份') # 设置x轴标签
plt.ylabel('数量') # 设置y轴标签
plt.title('各省订单数量排行前十') # 设置标题
plt.xticks(rotation=45) # 设置x轴刻度旋转角度
plt.savefig('./static/各省订单数量排行前十.png') # 保存图片

# 绘制年龄段分析的环形图
plt.figure(figsize=(8, 8)) # 设置画布大小
new_data = ["10-15岁", "16-20岁", "21-35岁", "36-40岁", "41-45岁", "46-50岁", "51-60岁", "61-65岁"]
plt.pie(df2['数量'], labels=new_data, autopct='%1.1f%%', startangle=90) # 绘制环形图
plt.title('年龄段分析') # 设置标题
plt.savefig('./static/年龄段分析.png') # 保存图片

# 绘制用户行为分析的环形图
plt.figure(figsize=(8, 8)) # 设置画布大小
labels = ["浏览", "加入购物车", "购买", "收藏"]
plt.pie(df3['数量'], labels=labels, autopct='%1.1f%%', startangle=90) # 绘制环形图
plt.title('用户行为分析') # 设置标题
plt.savefig('./static/用户行为分析.png') # 保存图片

# 绘制最高十类商品的饼图
plt.figure(figsize=(8, 8)) # 设置画布大小
labels = ["手机类", "日用品类", "服装类", "食品类", "家用电器类", "孕婴类", "计算机类", "汽车用品类", "珠宝类", "图书类"]
plt.pie(df4['数量'], labels=labels, autopct='%1.1f%%', startangle=90) # 绘制饼图
plt.title('最高十类商品') # 设置标题
plt.savefig('./static/最高十类商品.png') # 保存图片

# 绘制性别分析的柱形图
df5 = df5.groupby('性别').size() # 按性别分组并计数
plt.figure(figsize=(6, 6)) # 设置画布大小
plt.bar(df5.index, df5.values, color='blue') # 绘制柱形图
plt.xlabel('性别') # 设置x轴标签
plt.ylabel('数量') # 设置y轴标签
plt.title('性别分析') # 设置标题
plt.xticks([0, 1, 2], ['男', '女', '其他']) # 设置x轴刻度和标签
plt.savefig('./static/性别分析.png') # 保存图片

# 绘制用户评分分析的环形图
df6 = df6.groupby('用户评分').size() # 按用户评分分组并计数
plt.figure(figsize=(8, 8)) # 设置画布大小
labels = ['超级差', '很差', '有点差', '差', '中等', '好', '有点好', '很好', '超级好', 'wonderful']
plt.pie(df6.values, labels=labels, autopct='%1.1f%%', startangle=90) # 绘制环形图
plt.title('用户评分分析') # 设置标题
plt.savefig('./static/用户评分分析.png') # 保存图片

# 创建flask应用对象
app = Flask(__name__)
app.secret_key = 'secret' # 设置密钥

# 创建登录管理对象
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # 设置登录视图函数名称

# 创建用户类，继承UserMixin类
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# 创建用户字典，模拟数据库
users = {
    'admin': {'password': 'admin'},
    'user': {'password': 'user'}
}

# 创建留言列表，模拟数据库
messages = []

# 定义用户加载回调函数，根据用户id返回用户对象
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# 定义路由和视图函数
@app.route('/')
def index():
    # 渲染模板并返回
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # 如果是GET请求，渲染登录模板并返回
    if request.method == 'GET':
        return render_template('login.html')
    # 如果是POST请求，获取表单数据并验证
    username = request.form['username']
    password = request.form['password']
    if username in users and password == users[username]['password']:
        # 如果验证通过，创建用户对象并登录
        user = User(username)
        login_user(user)
        # 重定向到首页并返回
        return redirect(url_for('index'))
    else:
        # 如果验证失败，闪现错误信息并重定向到登录页面
        flash('用户名或密码错误')
        return redirect(url_for('login'))

@app.route('/logout')
@login_required # 需要登录才能访问
def logout():
    # 登出用户并重定向到首页
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # 如果是GET请求，渲染注册模板并返回
    if request.method == 'GET':
        return render_template('register.html')
    # 如果是POST请求，获取表单数据并验证
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    if username in users:
        # 如果用户名已存在，闪现错误信息并重定向到注册页面
        flash('用户名已存在')
        return redirect(url_for('register'))
    elif password != confirm_password:
        # 如果密码和确认密码不一致，闪现错误信息并重定向到注册页面
        flash('密码和确认密码不一致')
        return redirect(url_for('register'))
    else:
        # 如果验证通过，将用户信息添加到用户字典中
        users[username] = {'password': password}
        # 闪现成功信息并重定向到登录页面
        flash('注册成功，请登录')
        return redirect(url_for('login'))

@app.route('/各省订单数量排行前十')
@login_required # 需要登录才能访问
def order():
    # 渲染模板并返回
    return render_template('order.html')

@app.route('/年龄段分析')
@login_required # 需要登录才能访问
def age():
    # 渲染模板并返回
    return render_template('age.html')

@app.route('/用户行为分析')
@login_required # 需要登录才能访问
def behavior():
    # 渲染模板并返回
    return render_template('behavior.html')

@app.route('/最高十类商品')
@login_required # 需要登录才能访问
def product():
    # 渲染模板并返回
    return render_template('product.html')

@app.route('/性别分析')
@login_required # 需要登录才能访问
def gender():
    # 渲染模板并返回
    return render_template('gender.html')

@app.route('/用户评分分析')
@login_required # 需要登录才能访问
def rating():
    # 渲染模板并返回
    return render_template('rating.html')

@app.route('/留言板', methods=['GET', 'POST'])
@login_required # 需要登录才能访问
def board():
    if request.method == 'GET':
        # 如果是GET请求，渲染留言板模板并返回
        return render_template('board.html', messages=messages)
        # 如果是POST请求，获取表单数据并添加到留言列表中
    content = request.form['content']
    message = {'user': current_user.id, 'content': content}
    messages.append(message)
    # 重定向到留言板页面并返回
    return redirect(url_for('board'))
# 运行flask应用
if __name__ == '__main__':
    app.run(debug=True)

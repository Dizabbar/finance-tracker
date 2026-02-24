
import datetime 
import json
import os
def load_date():
    if os.path.exists('finance.json'):
        with open('finance.json', 'r', encoding = 'utf-8-sig') as f:
            return json.load(f)
    else:
        return {'balance': 0, 'income': [], 'transactions': [], 'savings': [], 'recurring': []}
def save_data(balance,income,transactions,savings,recurring):
    data = {
        'balance': balance,
        'income': income,
        'transactions': transactions,
        'savings': savings,
        'recurring': recurring
        }
    with open('finance.json', 'w', encoding = 'utf-8') as f:
        json.dump(data,f,ensure_ascii=False,indent=4)
def check_recurring(balance, income, transactions, savings, recurring):
    
    today = datetime.date.today()
    today_str = str(today)
    day = today.day
    for rec in recurring:
        if rec['day'] == day and rec['last_processed'] != today_str:
            if rec['auto_apply'] == True:
                balance = apply_recurring(rec,balance,income,transactions)
                rec['last_processed'] = today_str
                print(f'Автоматически добавлено: {rec['name']}')
            else:
                print(f'\nСегодня день для: {rec['name']}({rec['amount']} руб' )
                ans = input('Добавить ?  (д/н)')
                if ans.lower() == 'д': 
                    balance = apply_recurring(rec,balance,income,transactions)
                    rec['last_processed'] = today_str
                    print('Добавлено!')
    save_data(balance,income,transactions,savings, recurring)
    return balance
def apply_recurring(rec,balance,income,transactions):
    today_str = str(datetime.date.today())
    if rec['type'] == 'income':
        income.append({
            'name': rec['name'],
            'amount': rec['amount'],
            'date': today_str
            })
        balance += rec['amount']
    else:
        transactions.append({
            'amount': rec['amount'],
            'category': rec.get('category', 'Разное'),
            'date': today_str
            })
        balance -= rec['amount']
    return balance
def user_balance():
    data = load_date()
    balance = 0
    balance = data['balance']
    income = data['income']
    transactions = data['transactions']
    savings = data['savings']
    recurring = data['recurring']
    balance = check_recurring(balance, income, transactions, savings, recurring)
    date = str(datetime.date.today())

    while True:
        
        print('1.Добавление дохода')
        print('2.Просмотр доходов')
        print('3.Добавление расходов')
        print('4.Просмотр расходов')
        print('5.Баланс')
        print('6.Добавление сбережений')
        print('7.Статистика')
        print('8.Добавление регулярных операций')
        print('9.Просмотр регулярных операций')
        print('10.Стереть все данные')
        print('0.Выход')
        choise = int(input('Выбери пункт из меню 0-10: '))
        if choise == 0:
            save_data(balance,income,transactions,savings, recurring)
            break
        if choise == 1:
            name = input('Набери наименование дохода: ')
            amount = int(input('Набери сумму дохода: '))
            today = str(datetime.date.today())
            income.append({'name': name, 'amount': amount, 'date': today})
            balance += amount
            save_data(balance,income,transactions,savings, recurring)
        if choise == 2:
            for inc in income:
                print(f'{inc['date']} | {inc['name']}: {inc['amount']} rub')
        if choise == 3:
            category = input('Набери наименование расхода: ')
            amount = int(input('Набери сумму расхода: '))
            transactions.append({'amount': amount, 'category': category, 'date':str(datetime.date.today())})
            balance -= amount
            save_data(balance,income,transactions,savings, recurring)
        if choise == 4:
            for t in transactions:
                print(f'{t['Amount']} rub - {t['category']} date - {t[str(datetime.date.today())]}')
        if choise == 5:
            print(balance)
        if choise == 6:
            while True:
                print('1.Просмотр суммы накоплений')
                print('2.Добавление в накопление')
                print('0.Выход')
                choise_saving = int(input('Выбери пунк из меню 0-2: '))
                if choise_saving == 0:
                    break
                elif choise_saving == 1:
                    print(savings)
                elif choise_saving == 2:
                    amount_saving = int(input('Введите сумму: '))
                    
                    savings.append({'amount': amount_saving, 'date': str(datetime.date.today())})
             
                    save_data(balance,income,transactions,savings, recurring)
        if choise == 7:
            ym = input('Введите год и месяц (ГГГГ-ММ): ')
            month_income = filter_by_month(income,ym)
            month_expense = filter_by_month(transactions,ym)

            total_income = sum(inc['amount'] for inc in month_income)
            total_expense = sum(inc['amount'] for inc in month_expense)
            
            print(f'\n stats in month')
            print(f'income: {total_income} rub')
            print(f'expense: {total_expense} rub')

            if total_expense > 0:
                print('\n expense in category')
                categories = { }
                for exp in month_expense:
                    cat = exp['category']
                    categories[cat] = categories.get(cat, 0) + exp['amount']

                sorted_cats = sorted(categories.items(),key=lambda x: x[1], reverse=True)
                for cat, amount in sorted_cats:
                    percent = (amount / total_expense) * 100
                    bar = '|' * int(percent // 5)
                    print(f'{cat:15} {amount:7} rub {bar} {percent:.1f}%')
            else:
                print('rashodv ne bilo')
        elif choise == 8:
            print('\n---Adding a regular operation---')
            type_op = input('Тип (income/expense):').lower()
            name = input('Название: ')
            amount = int(input('Сумма: '))
            day = int(input('День месяца(1-31):'))
            auto = input('Добавлять автоматически? (да/нет)').lower() == 'да'
            category = None
            if type_op == 'expense':
                category = input('Категория: ')
            new_id = 1
            if recurring:
                new_id = max(r['id'] for r in recurring) + 1
            rec = {'id': new_id, 
                   'type': type_op, 
                   'name': name, 
                   'amount': amount, 
                   'day': day, 
                   'last_processed': None, 
                   'auto_apply': auto
                   }
            if category: 
                rec['category'] = category
            recurring.append(rec)
            save_data(balance,income,transactions,savings,recurring)
            print('Регулярная операция выполнена')
        elif choise == 9:
           print("\n--- Регулярные операции ---")
           for rec in recurring:
               auto_str = "авто" if rec['auto_apply'] else "с подтверждением"
               last = rec['last_processed'] if rec['last_processed'] else "никогда"
               print(f"[{rec['id']}] {rec['name']} — {rec['amount']} руб, день {rec['day']}, {auto_str}, последний раз: {last}")
        elif choise == 10:
            balance = 0
            income = []
            transactions = []
            savings = []
            recurring = []
            save_data(balance,income,transactions,savings, recurring)
            break

def filter_by_month(items,year_month):
    result = []
    for item in items:
        if item['date'].startswith(year_month):
            result.append(item)
    return result


          
user_balance()

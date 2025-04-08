from datetime import datetime

# Клас, який відповідає за прийняття значень контакту
class Contact:
  def __init__(self, name, phone=None, address=None, email=None, birthday=None):
    self._name = None
    self._phone = None
    self._address = None
    self._email = None
    self._birthday = None

    # виклик сеттерів
    self.name = name
    self.phone = phone
    self.address = address
    self.email = email
    self.birthday = birthday

  # парсинг дати народження
  def parse_birthday(self, bday):
    if isinstance(bday, str):
      try:
        return datetime.strptime(bday, "%d-%m-%Y").date()
      except ValueError:
        return None
    return bday

  # текстовий вивід
  def __str__(self):
    def show(value):
      return value if value else "Empty"
    
    bday = self._birthday.strftime("%d-%m-%Y") if self._birthday else "Empty"
    return f"Name: {self._name} | 📞Phone: {show(self._phone)} | 🏠Address: {show(self._address)} | ✉️Email: {show(self._email)} | 🎂Birthday: {bday}"
  
  def __repr__(self):
    return f"Contact(name='{self._name}')"
  

  # Геттери та сеттери
  @property
  def name(self):
    return self._name 
  
  @name.setter
  def name(self, value):
    self._name = value

  @property
  def phone(self):
    return self._phone
  
  @phone.setter
  def phone(self, value):
    self._phone = value

  @property
  def address(self):
    return self._address
  
  @address.setter
  def address(self, value):
    self._address = value

  @property
  def email(self):
    return self._email
  
  @email.setter
  def email(self, value):
    self._email = value

  @property
  def birthday(self):
    return self._birthday
  
  @birthday.setter
  def birthday(self, value):
    self._birthday = self.parse_birthday(value)



# Клас, який відповідає за прийняття значень нотаток
class Note:
  def __init__(self, text):
    self._text = text
    self._created_date = datetime.today()
  
  # текстовий вивід
  def __str__(self):
    return f"Note:\n{self._text}\n📅 Created: {self._created_date.strftime('%d-%m-%Y %H:%M')}"
  
  def __repr__(self):
    return f"Note(text='{self._text[:15]}...')"
  
  # Геттери та сеттери
  @property
  def text(self):
    return self._text
  
  @text.setter
  def text(self, value):
    self._text = value

  @property
  def created_date(self):
    return self._created_date
  
  
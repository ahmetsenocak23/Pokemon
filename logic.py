import aiohttp , random , asyncio # Eşzamansız HTTP istekleri için bir kütüphane
from datetime import timedelta, datetime 
import time

class Pokemon:
    pokemons = {}
    # Nesne başlatma (kurucu)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.hp = random.randint(50,100)
        self.power = random.randint(1,20)
        self.last_feed_time = datetime.now()
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]

    async def get_name(self):
        # PokeAPI aracılığıyla bir pokémonun adını almak için eşzamansız bir yöntem
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API'si
        async with aiohttp.ClientSession() as session:  # Bir HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve kodunun çözülmesi
                    return data['forms'][0]['name']  # Bir Pokémon'un adını döndürme
                else:
                    return "Pokemon Yanıt Vermedi :( , Lütfen Tekrar Deneyin "  # İstek başarısız olursa varsayılan adı döndürür

    async def info(self):
        # Pokémon hakkında bilgi döndüren bir metot
        if not self.name:
            self.name = await self.get_name()  # Henüz yüklenmemişse bir adın geri alınması
        return f"Pokémonunuzun ismi: {self.name} \nPokemonunuzun Sağlığı: {self.hp}\n Pokemonunuzun Gücü: {self.power}"  # Pokémon'un adını içeren dizeyi döndürür

    async def show_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API'si
        async with aiohttp.ClientSession() as session:  # Bir HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve kodunun çözülmesi
                    return data['sprites']['front_default']  # Bir Pokémon'un adını döndürme
                else:
                    return "Pikachu"  # İstek başarısız olursa varsayılan adı döndürür
                


    async def attack(self, target):
        if isinstance(target, Wizard):  # Enemy'nin bir Wizard veri tipi olduğunu (Büyücü sınıfının bir örneği olduğunu) kontrol etme
            chance = random.randint(1, 5) 
            if chance == 1:
                return "Sihirbaz Pokémon, savaşta bir kalkan kullanıldı!"
            
        if self.hp == 0:
            return "üzgünüm canınız 0 olduğu için saldırı yapamazsınız"

        elif target.hp > self.power:
            target.hp -= self.power
            return f"@{self.pokemon_trainer} , @{target.pokemon_trainer} oyuncusuna saldırdı, \n@{target.pokemon_trainer} oyuncusunun sağlık durumu {target.hp}"
        else:
            target.hp = 0
            return f"{self.pokemon_trainer} , {target.pokemon_trainer} oyuncusunu yendi"
        

    async def feed(self, feed_interval=20, hp_increase=10):
        current_time = datetime.now()
        delta_time = timedelta(seconds=feed_interval)
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Pokémon'un sağlığı geri yüklenir. Mevcut sağlık: {self.hp}"
        else:
            return f"Pokémonunuzu şu zaman besleyebilirsiniz: {current_time+delta_time}"
            

class Wizard(Pokemon):
    async def attack(self, target):
        return await super().attack(target)
    
    async def feed(self):
        return await super().feed(feed_interval=10 , hp_increase= 10)
    
    

class Fighter(Pokemon):
    async def attack(self, enemy):
        if self.hp == 0:
            return "Üzgünüm Canınız 0 Olduğu için Saldırı Yapamazsınız"
        else:
            super_power = random.randint(5, 15)  
            self.power += super_power
            sonuç = await super().attack(enemy)  
            self.power -= super_power
            return sonuç + f"\nDövüşçü Pokémon süper saldırı kullandı. Eklenen güç: {super_power}"
    
    async def feed(self):
        return await super().feed(feed_interval=20 , hp_increase= 20)   
    


if __name__ == '__main__':
    async def main():
     
        pokemon = Fighter('𝐀𝐡𝐦𝐞𝐭')
        print(await pokemon.info())
        print(await pokemon.feed())
        time.sleep(20)
        print(await pokemon.feed())

       



        
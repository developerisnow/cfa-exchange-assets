# Agenda
- Yury, Aleksandr - expects Alex share his vision based on his 15h research
- Alex planned to show 
# Notes written by Alex during the meeting 
Disclaimer! Alex made random notes during the meeting, it's not full ending correct sentences, it's just a spontaneous notes which he did during screensharing, more details and facts, bullets, action points and all insights must to be extracted from a meeting recording transcript.
Alex recorded transcript is not full because of extra-sounds at cafe and we expect full recording from the Yury.
## Alex Plans
- [ ] show Competitors
- [ ] show C4, Domain
- [ ] обсудить путь Next Actions, Kickoff tasks, DoD

## Questions
1. Погружались ли во что?  И что начинали делать?
2. Какой самый главный или несколько Epic

## Key Ideas
- [ ] {FRONTEND AREA} параллельно запустить процесс Разработки **PLATFORM_FRONTEND**  на основе structure.xlsx + competitor+screenshots in {lovable}
	- [ ] инвестора
	- [ ] эмитент (юрик)
	- [ ] backoffice (админка)
- [ ] {BACKEND AREA}
	- [ ] архитектура прорабатываем на оснвое доменов сколько будет ключевых микросервисов и на чем пистаь
		- [ ]  Подход к разработке через Spec Driven Development SDD Flow: PRD -> TDD -> Backlog (Epic->Features->Story->Tasks)
		- [ ] Backend microservices - сколько их, какого размера
		- [ ] Сколько будет 3rd party - Готового решения
	- предпочтения
		- .NET, Golang (Blockchain)
		- Typescript,Python,Golang

## Investigation competitors
- network  
## 3rd party services list
1. Blockchain (DLT / Ledger)
2. Bank (DvP) 
3. KYC
	1. Госуслуги
4. KYB
5. ЭДО


## Next Actions
- Alex
  - [ ] выгрузить текущие материалы в Gitlab
  - [ ] Провести дальнейшее погружение и ресерч с целью DoD(deliverable) схемы на дальнейшую архитектуру в схемах C4, DDD, high-level для дальнейшего согласования/обсуждения
    - [ ] Для этой задачи необходимы/полезны  сredentials в личные кабинеты конкурентов
    - [ ] Названия сервисов для интеграции и credentials/api docs/keys если есть
    - [ ] проанализировать еще входящие материалы PDF,etc и перевести в LLM-удобоваримый вариант для интеграции в наш SDD Flow.
  - [ ] Продолжать Specs Driven Development в Gitlab
- Aleksandr
  - [ ] выгрузить материалы в Gitlab
- Yury
	- [ ] поделиться записью-встречи-от-20251103
	- [ ] дать credentials от аккаунтуов конкурентов (всего конкурентов в наших док-тах 20 штук, Юрий даст сколько есть)
	- [ ] предоставить список сервисов с которыми будет/предполагается интеграция с отсылками на какой стадии с каждым 
		- например, с кем-то уже есть договора и можно дать API keys доступы в песочницу, с кем-то лишь соглашения о намерениях, с кем-то еще не общались и рассматривается как вариант, а какой-то тип решения нужно лишь еще отыскать
		- На всякий случай дублирую из входящей информации предварительные доменные сущности: DLT Registry(Blockchain), Identidy&KYC,Tokenization, Settlement-and-DvP(Banks),PaymentsProviders,Custody/Wallets,Complience-and-AML

### Telegram adapted
````telegram
2025-11-03 Meeting  Next Actions

Alex
1. выгрузить текущие материалы в Gitlab
2. Провести дальнейшее погружение и ресерч с целью DoD(deliverable) схемы на дальнейшую архитектуру в схемах C4, DDD, high-level для дальнейшего согласования/обсуждения
2.1.  (⌛️Yury)  Для этой задачи необходимы/полезны  сredentials в личные кабинеты конкурентов
2.2. (⌛️Yury) Названия сервисов для интеграции и credentials/api docs/keys если есть
2.3. проанализировать еще входящие материалы PDF,etc и перевести в LLM-удобоваримый вариант для интеграции в наш SDD Flow.
3. Продолжать Specs Driven Development в Gitlab

Aleksandr
1. выгрузить материалы, src в Gitlab
2. Дальше он допишет

Yury
1. ✅ поделиться записью-встречи-от-20251103
2. дать credentials от аккаунтуов конкурентов (всего конкурентов в наших док-тах 20 штук, Юрий даст сколько есть)
3. предоставить список сервисов с которыми будет/предполагается интеграция с отсылками на какой стадии с каждым 
- например, с кем-то уже есть договора и можно дать API keys доступы в песочницу, с кем-то лишь соглашения о намерениях, с кем-то еще не общались и рассматривается как вариант, а какой-то тип решения нужно лишь еще отыскать
- На всякий случай дублирую из входящей информации предварительные доменные сущности: DLT Registry(Blockchain), Identidy&KYC,Tokenization, Settlement-and-DvP(Banks),PaymentsProviders,Custody/Wallets,Complience-and-AML
````
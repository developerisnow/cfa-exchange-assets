

› what git branch now on `uk1` used? Там поднято все же в очень старой ветке main,  и кажется без git нормального              
  Есть огромнейшие изменения на 1000+ файлов как мне лучше там сделать деплой и обезопасить себя чтобы не сломать то что там отлично работает?                                                                                                                 

  вот тебе для исследования код                                

  ```                                                          
  [08:58] user@eywa-ubuntu-8gb-hel1-2 ois-cfa (dev-cfa2) $ git pull                                                            
  Already up to date.                                          
  [08:59] user@eywa-ubuntu-8gb-hel1-2 ois-cfa (dev-cfa2) $ git worktree add ../wt__ois-cfa__develop develop                    
  Preparing worktree (checking out 'develop')                  
  HEAD is now at 077c9bf fix(test) playwright                  
  [08:59] user@eywa-ubuntu-8gb-hel1-2 ois-cfa (dev-cfa2) $ cd ../wt__ois-cfa__develop/                                         
  [08:59] user@eywa-ubuntu-8gb-hel1-2 wt__ois-cfa__develop (develop) $ git pull                                                
  Updating 077c9bf..973c5f1                                    
  Fast-forward                                                 
   artifacts/AlexA/architecture/ois-cfa.reposcan.json                  | 562 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++                                                      
   artifacts/AlexA/architecture/project-C4.diagram.md                  | 361 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++                                                                                                  
   artifacts/AlexA/architecture/project-reposcan.md                    |  24 ++++++                                            
   backlog/visual/20251126-1500-visualization-for-the-call.diagrams.md | 810 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
  ++                                                           
   backlog/visual/20251126-1505-visualization-v2-before-call.md        | 263 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++                                                                                                                        
   5 files changed, 2020 insertions(+)                         
   create mode 100644 artifacts/AlexA/architecture/ois-cfa.reposcan.json                                                       
   create mode 100644 artifacts/AlexA/architecture/project-C4.diagram.md                                                       
   create mode 100644 artifacts/AlexA/architecture/project-reposcan.md                                                         
   create mode 100644 backlog/visual/20251126-1500-visualization-for-the-call.diagrams.md                                      
   create mode 100644 backlog/visual/20251126-1505-visualization-v2-before-call.md                                             
  [08:59] user@eywa-ubuntu-8gb-hel1-2 wt__ois-cfa__develop (develop) $ pwd                                                     
  /home/user/__Repositories/yury-customer/prj_Cifra-rwa-exachange-assets/repositories/customer-gitlab/wt__ois-cfa__develop     
  [08:59] user@eywa-ubuntu-8gb-hel1-2 wt__ois-cfa__develop (develop) $                                                         

  [08:59] user@eywa-ubuntu-8gb-hel1-2 wt__ois-cfa__develop (develop) $ git worktree add ../wt__ois-cfa__main main              
  Preparing worktree (checking out 'main')                     
  HEAD is now at 35a15d1 docs(reposcan): add Shotgun SDD JSON (ois-cfa.shtgn.reposcan.json)                                    
  [09:00] user@eywa-ubuntu-8gb-hel1-2 wt__ois-cfa__develop (develop) $                                                         
  ```                                                          
  внимание я не прошу merge я обсуждаю как лучше сделать deploy, уточняю есть ли там в git изменения какими командами ты бы все проверил и потом я                                                                                                             
  как там все организовано                                     


• Ran bash -lc 'ssh -p 51821 root@185.168.192.214 "cd /opt/ois-cfa && pwd && git branch --show-current && git status -sb || echo no-git"'                                                                                                                      
  └ /opt/ois-cfa                                               
    fatal: not a git repository: /opt/ois-cfa/../../../.git/modules/repositories/customer-gitlab/ois-cfa                       
    no-git                                                     

─ Worked for 1m 24s ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

• Отвечаю по фактам и с планом деплоя, без мерджа.             

  ———                                                          

  1. Что сейчас на UK1                                         

  Я проверил напрямую:                                         

  ssh -p 51821 root@185.168.192.214 \                          
    'cd /opt/ois-cfa && pwd && git branch --show-current && git status -sb || echo no-git'                                     

  Ответ:                                                       

  - pwd → /opt/ois-cfa                                         
  - git ругается: fatal: not a git repository: /opt/ois-cfa/../../../.git/modules/repositories/customer-gitlab/ois-cfa         

  То есть:                                                     

  - На UK1 лежит снимок дерева (скорее всего rsync из монорепы), а не нормальный git‑клон.                                     
  - .git внутри ссылается на путь вида ../../../.git/modules/..., который существует на eywa1, но не существует на UK1.        
  - Поэтому на UK1 нет активной ветки вообще – это просто «распакованный main/deploy времён CFA1/первого UK1 деплоя».          

  Вывод: то, что сейчас работает на UK1, – это «замороженный» снапшот кода + правильные .env/docker‑volume'ы, но git‑историю этот сервер не отражает.                                                                                                          

  ———                                                          

  2. Что бы я проверил, не трогая код                          

  Смысл: считать UK1 как runtime‑машину, а всю «правду» о коде держать на eywa1/GitLab.                                        

  На UK1:                                                      

  # 1) понять, что реально крутится                            
  cd /opt/ois-cfa                                              
  docker compose ps                                            
  docker compose config | head -40      # быстренько глянуть, какие файлы compose подхватывает                                 

  # 2) зафиксировать текущее состояние для отката              
  ls -1 .env docker-compose*.yml ops/ docs/deploy apps/*/.env* 2>/dev/null                                                     

  На eywa1 (твоя рабочая копия):                               

  cd prj_Cifra-rwa-exachange-assets/repositories/customer-gitlab/ois-cfa                                                       

  # Понять, где живёт актуальный код                           
  git branch -vv              # deploy / infra.defis.deploy / develop / main                                                   
  git log --oneline -5 deploy                                  
  git log --oneline -5 infra.defis.deploy                      
  git log --oneline -5 develop                                 

  # Оценить масштаб расхождений:                               
  git diff --shortstat origin/main..infra.defis.deploy         
  git diff --shortstat origin/deploy..infra.defis.deploy       
  git diff --shortstat origin/develop..infra.defis.deploy      

  Эти команды дают тебе картинку:                              

  - от какой ветки мы реально хотим деплоиться (сейчас это логичнее всего infra.defis.deploy, потому что там и infra, и твои UK1 runbook’и),                                                                                                                   
  - насколько далеко эта ветка ушла от старого main/deploy, который «заморожен» на UK1.                                        

  ———                                                          

  3. Стратегия деплоя, чтобы ничего не сломать                 

  Ключевой принцип: UK1 никогда не является источником правды по коду, только по конфигам и данным. Код всегда берём из GitLab, а на UK1:                                                                                                                      

  - делаем бэкап,                                              
  - кладём новый код в отдельную папку,                        
  - переключаем docker‑compose,                                
  - умеем откатиться.                                          

  ### Шаг 0. Не трогаем старый /opt/ois-cfa напрямую           

  На UK1:                                                      

  ssh -p 51821 root@185.168.192.214                            

  # 0.1. Зафиксировать бэкап текущей папки                     
  cd /opt                                                      
  tar czf ois-cfa_$(date +%Y%m%d-%H%M)_backup.tgz ois-cfa      

  # 0.2. Сохранить отдельно env/override для удобства          
  cp -a ois-cfa/.env ois-cfa.env.backup 2>/dev/null || true    
  cp -a ois-cfa/docker-compose*.yml ois-cfa.compose.backup/ 2>/dev/null || true                                                

  Теперь, даже если новый деплой «взорвётся», у тебя есть:     

  - архив старого дерева,                                      
  - старые .env и compose.                                     

  ### Шаг 1. Сделать нормальный git‑клон на UK1                

  Предлагаю не чинить существующий .git, а положить новый клон рядом:                                                          

  cd /opt                                                      
  git clone git@git.telex.global:npk/ois-cfa.git -b infra.defis.deploy ois-cfa_new                                             

  cd ois-cfa_new                                               
  git status -sb   # должен быть чистый клон infra.defis.deploy

  Дальше переносим только то, что специфично для UK1:          

  # .env / overrides / портальные env.local из старой папки    
  cp ../ois-cfa/.env . 2>/dev/null || true                     
  cp ../ois-cfa/docker-compose*.yml . 2>/dev/null || true      
  cp -a ../ois-cfa/apps/portal-issuer/.env.local apps/portal-issuer/.env.local 2>/dev/null || true                             
  cp -a ../ois-cfa/apps/portal-investor/.env.local apps/portal-investor/.env.local 2>/dev/null || true                         
  cp -a ../ois-cfa/apps/backoffice/.env.local apps/backoffice/.env.local 2>/dev/null || true                                   

  Важно: таким образом ты получаешь нормальный git‑репозиторий на UK1, отслеживающий infra.defis.deploy, но не ломая старый /opt/ois-cfa.                                                                                                                      

  ### Шаг 2. Прогнать compose в новой папке                    

  На UK1:                                                      

  cd /opt/ois-cfa_new                                          

  # Проверить, что compose читает то, что нужно:               
  docker compose config >/tmp/ois-cfa_new.compose.yml          

  # Остановить старый стек, но не удалять volumes:             
  cd /opt/ois-cfa                                              
  docker compose down                                          

  # Запустить новый стек из новой папки:                       
  cd /opt/ois-cfa_new                                          
  docker compose up -d                                         

  При проблемах:                                               

  - если контейнеры не поднимаются или healthchecks падают — остановить новый стек и вернуться на старый:                      

  cd /opt/ois-cfa_new                                          
  docker compose down                                          

  cd /opt/ois-cfa                                              
  docker compose up -d                                         

  ### Шаг 3. После успешного smoke – переключить папку         

  Если всё ок (health готов, порталы логинятся):               

  - либо переименовать:                                        

  cd /opt                                                      
  mv ois-cfa ois-cfa_old_$(date +%Y%m%d-%H%M)                  
  mv ois-cfa_new ois-cfa                                       

  - либо просто помнить, что рабочий путь теперь /opt/ois-cfa_new и поправить systemd/cron/документацию.                       

  Лучше всё‑таки переименовать, чтобы runbook’и оставались валидными (/opt/ois-cfa как canonical путь).                        

  ———                                                          

  4. Что ещё проверить перед деплоем                           

  На eywa1, до того как вообще трогать UK1, как senior я бы:   

  cd prj_Cifra-rwa-exachange-assets/repositories/customer-gitlab/ois-cfa                                                       

  # 1. Убедиться, что infra.defis.deploy в порядке             
  git checkout infra.defis.deploy                              
  git pull origin infra.defis.deploy                           

  # 2. Минимальный тестовый пояс:                              
  dotnet test services/settlement/settlement.Tests.csproj   # или ближайший smoke                                              
  npm test --prefix tests/e2e-playwright                    # если хотим авторизацию проверить                                 

  # 3. Быстрый локальный docker-compose smoke (по желанию)     
  docker compose -f docker-compose.yml -f docker-compose.services.yml config >/tmp/compose.check.yml                           

  Только после этого я бы ехал на UK1 и делал схему «backup → clone → перенести env → compose up».                             

  ———                                                          

  5. Ответ на твой вопрос в лоб                                

  > what git branch now on uk1 used?                           

  Фактически никакая: /opt/ois-cfa на UK1 сейчас не является валидным git‑репо, это просто рабочее дерево (старый main/deploy снапшот). Для нового деплоя надо:                                                                                                

  - считать UK1 чисто runtime‑хостом,                          
  - сделать новый git clone нужной ветки (infra.defis.deploy или develop) в отдельную папку,                                   
  - аккуратно перенести env/compose, прогнать docker, и только потом переключиться.                                            

  Так ты не сломаешь то, что уже отлично работает, и в любой момент сможешь откатиться на архив или на старую папку.           

───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

• Compact task completed                                       

───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

• Коротко:                                                     

  1. Какая ветка сейчас “на UK1”                               

  - На UK1 в /opt/ois-cfa по факту нет нормального git‑репозитория: .git там — это ссылка на путь на eywa1, которого на UK1 нет.                                                                                                                               
  - Поэтому никакая ветка сейчас не “активна”. Это просто “замороженный снапшот” старого состояния (по содержимому ближе к старому main/deploy), который дальше руками донастраивали (.env, docker-compose, nginx и т.п.).                                     
  - Все живое ветвление (develop, infra.defis.deploy, dev-cfa2) — только на eywa1 в /home/user/.../ois-cfa и worktree’ах.      

  Если хочешь сам убедиться на UK1:                            

  ssh uk1                                                      
  cd /opt/ois-cfa                                              
  ls -a                                                        
  cat .git        # увидишь ссылку на путь на eywa1, git status тут не сработает                                               

  2. Какими командами я бы проверял, что и как организовано    

  На eywa1 (нормальный репозиторий):                           

  - Посмотреть ветки и активную:                               

    cd /home/user/__Repositories/yury-customer/prj_Cifra-rwa-exachange-assets/repositories/customer-gitlab/ois-cfa             
    git branch -vv                                             
    git remote -v                                              
  - Понять различия между ветками, от которых потенциально будем деплоиться (например, infra.defis.deploy, develop, dev-cfa2): 

    git fetch --all --prune                                    
    git diff --stat origin/infra.defis.deploy..origin/develop  
    git diff --stat origin/infra.defis.deploy..dev-cfa2        
  - Найти последний коммит, от которого, скорее всего, собирали UK1 (ищем совпадения по файлам/датам, если нужно):             

    # пример: смотрим историю нужных файлов docker-compose / Program.cs                                                        
    git log --oneline -- apps/api-gateway/appsettings.json     
    git log --oneline -- docker-compose.yml                    

  На uk1:                                                      

  - Проверить, что git “сломан” и локальных незакоммиченных изменений мы не увидим через git:                                  

    ssh uk1                                                    
    cd /opt/ois-cfa                                            
    cat .git          # покажет путь на eywa1                  
    # просто смотрим файловую структуру                        
    ls                                                         
    ls docker-compose*.yml                                     
  - Зафиксировать текущее рабочее состояние перед любыми экспериментами (для себя):                                            

    # быстрый “снапшот” списка файлов и хэшей                  
    find . -type f -maxdepth 5 -print0 | xargs -0 md5sum > /root/ois-cfa.snapshot.md5                                          

  3. Как безопасно деплоить новую версию, не ломая рабочую     

  Идея: две папки на UK1 + явный “release/uk1”‑бранч на eywa1, никакого “в лоб поверх /opt/ois-cfa`.                           

  Шаги (high-level):                                           

  1. Выбрать базовую ветку для релиза на eywa1 (скорее всего infra.defis.deploy или твой dev-cfa2):                            

     git checkout infra.defis.deploy   # или dev-cfa2          
     git pull                                                  
     git status                                                
     git log -5 --oneline                                      
     Если нужно – сделать от неё отдельную релиз‑ветку, чтобы не мешать дальнейшей разработке:                                 

     git checkout -b release/uk1-2025-11-27                    
     git checkout -b release/uk1-2025-11-27                    
  2. Подготовить новый деплой‑каталог на UK1 (ничего не трогая в текущем /opt/ois-cfa):                                        
      - На uk1:                                                

        ssh uk1                                                
        mkdir -p /opt/ois-cfa_releases                         
        cd /opt/ois-cfa_releases                               
        git clone git@...:npk/ois-cfa.git ois-cfa_2025-11-27   
        cd ois-cfa_2025-11-27                                  
        git checkout release/uk1-2025-11-27   # или нужную ветку                                                               
      - Скопировать только нужные конфиги из текущего живого снапшота:                                                         

        cd /opt                                                
        rsync -a ois-cfa/.env ois-cfa_releases/ois-cfa_2025-11-27/.env                                                         
        rsync -a ois-cfa/docker-compose*.yml ois-cfa_releases/ois-cfa_2025-11-27/                                              
        rsync -a ois-cfa/apps/*/.env.local ois-cfa_releases/ois-cfa_2025-11-27/apps/ 2>/dev/null || true                       
  3. Прогнать сборку и health‑чеки в новом каталоге (ещё без переключения прод‑трафика):                                       

     cd /opt/ois-cfa_releases/ois-cfa_2025-11-27               
     docker compose build         # или только нужные сервисы  
     docker compose up -d                                      
     # локальные чеки                                          
     curl -f http://localhost:5000/health || echo "api-gateway not healthy"                                                    
     curl -f http://localhost:8080/health/ready || echo "kc not ready"                                                         

     Если хочешь совсем без риска – временно поднять это с другими портами (override‑файл), проверить Playwright’ом, и только потом пересобрать/перезапустить на боевых портах.                                                                                
  4. Сделать “swap” только когда новый стек стабилен:          
     Самый простой вариант — остановить старый стек и запустить новый теми же командами/портами, что и сейчас (системд‑юниты или tmux‑сессию обновить так, чтобы они смотрели на новый путь). При проблемах у тебя останется старый /opt/ois-cfa для быстрого  
     отката:                                                   

     # rollback-пример                                         
     mv /opt/ois-cfa /opt/ois-cfa_bad_2025-11-27               
     mv /opt/ois-cfa_releases/ois-cfa_2025-11-27 /opt/ois-cfa  
     # и затем обычный docker compose up -d в новом /opt/ois-cfa                                                               
  5. Каталог / ветка для следующего релиза не трогаем:         
      - Продолжать разрабатывать на infra.defis.deploy / dev-cfa2 на eywa1.                                                    
      - Для каждого следующего деплоя повторять паттерн “новая release‑ветка → новый release‑каталог на UK1 → health‑чеки → swap”.                                                                                                                             

  Итого:                                                       

  - Сейчас на UK1 нет активной git‑ветки, а просто старый снапшот.                                                             
  - Проверить это можно через cat .git на UK1.                 
  - Для безопасного деплоя новых 1000+ изменений: использовать release‑ветку + отдельный каталог на UK1 + чёткий план rollback’а, не переписывая живой /opt/ois-cfa напрямую.                                                                                  


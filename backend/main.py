from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base, SessionLocal
from app.routers import channels, categories, streams, auth
from app.models.category import Category
from app.models.channel import Channel
from app.models.user import User

# Crear tablas en la BD
Base.metadata.create_all(bind=engine)

# Seed automático si no hay datos
def seed_db():
    db = SessionLocal()
    try:
        if db.query(Category).count() == 0:
            # Crear categorías
            categories_data = [
                Category(name="Deportes", slug="deportes", icon="fa-futbol"),
                Category(name="Reality", slug="reality", icon="fa-tv"),
            ]
            db.add_all(categories_data)
            db.flush()

            # Crear canales (103 canales)
            channels_data = [
                Channel(name="ESPN 2", slug="espn2mx", stream_url="https://tvtvhd.com/vivo/canales.php?stream=espn2mx", logo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/ESPN_wordmark.svg/200px-ESPN_wordmark.svg.png", category_id=1, is_active=True),
                Channel(name="ESPN 3", slug="espn3mx", stream_url="https://tvtvhd.com/vivo/canales.php?stream=espn3mx", logo_url=None, category_id=1, is_active=True),
                Channel(name="ESPN 4", slug="espn4mx", stream_url="https://tvtvhd.com/vivo/canales.php?stream=espn4mx", logo_url=None, category_id=1, is_active=True),
                Channel(name="ESPN 5", slug="espn5", stream_url="https://tvtvhd.com/vivo/canales.php?stream=espn5", logo_url=None, category_id=1, is_active=True),
                Channel(name="ESPN 6", slug="espn6", stream_url="https://tvtvhd.com/vivo/canales.php?stream=espn6", logo_url=None, category_id=1, is_active=True),
                Channel(name="ESPN 7", slug="espn7", stream_url="https://tvtvhd.com/vivo/canales.php?stream=espn7", logo_url=None, category_id=1, is_active=True),
                Channel(name="DSports", slug="dsports", stream_url="https://tvtvhd.com/vivo/canales.php?stream=dsports", logo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/DirectTV_Sports_logo.png/200px-DirectTV_Sports_logo.png", category_id=1, is_active=True),
                Channel(name="DSports+", slug="dsportsplus", stream_url="https://tvtvhd.com/vivo/canales.php?stream=dsportsplus", logo_url=None, category_id=1, is_active=True),
                Channel(name="DSports 2", slug="dsports2", stream_url="https://tvtvhd.com/vivo/canales.php?stream=dsports2", logo_url=None, category_id=1, is_active=True),
                Channel(name="Test Channel", slug="test-channel", stream_url="https://example.com/stream", logo_url=None, category_id=1, is_active=True),
                Channel(name="ESPN 2", slug="espn2mx1", stream_url="https://tvtvhd.com/vivo/canales.php?stream=espn2mx", logo_url=None, category_id=1, is_active=True),
                Channel(name="ESPN 3", slug="espn3mx1", stream_url="https://tvtvhd.com/vivo/canales.php?stream=espn3mx", logo_url=None, category_id=1, is_active=True),
                Channel(name="ESPN 4", slug="espn4mx1", stream_url="https://tvtvhd.com/vivo/canales.php?stream=espn4mx", logo_url=None, category_id=1, is_active=True),
                Channel(name="ESPN 5", slug="espn51", stream_url="https://tvtvhd.com/vivo/canales.php?stream=espn5", logo_url=None, category_id=1, is_active=True),
                Channel(name="ESPN 6", slug="espn61", stream_url="https://tvtvhd.com/vivo/canales.php?stream=espn6", logo_url=None, category_id=1, is_active=True),
                Channel(name="ESPN 7", slug="espn71", stream_url="https://tvtvhd.com/vivo/canales.php?stream=espn7", logo_url=None, category_id=1, is_active=True),
                Channel(name="DSports 2", slug="dsports21", stream_url="https://tvtvhd.com/vivo/canales.php?stream=dsports2", logo_url=None, category_id=1, is_active=True),
                Channel(name="GOLTV", slug="goltv", stream_url="https://tvtvhd.com/vivo/canales.php?stream=goltv", logo_url=None, category_id=1, is_active=True),
                Channel(name="VTV Plus", slug="vtvplus", stream_url="https://tvtvhd.com/vivo/canales.php?stream=vtvplus", logo_url=None, category_id=1, is_active=True),
                Channel(name="ECDF LigaPro (eventos)", slug="ecdfligaproeventos", stream_url="https://tvtvhd.com/vivo/canales.php?stream=ecdfligapro(eventos)", logo_url=None, category_id=1, is_active=True),
                Channel(name="Fox Sports", slug="foxsports", stream_url="https://tvtvhd.com/vivo/canales.php?stream=foxsports", logo_url=None, category_id=1, is_active=True),
                Channel(name="Fox Sports 2", slug="foxsports2", stream_url="https://tvtvhd.com/vivo/canales.php?stream=foxsports2", logo_url=None, category_id=1, is_active=True),
                Channel(name="Fox Sports 3", slug="foxsports3", stream_url="https://tvtvhd.com/vivo/canales.php?stream=foxsports3", logo_url=None, category_id=1, is_active=True),
                Channel(name="TNT Sports", slug="tntsports", stream_url="https://tvtvhd.com/vivo/canales.php?stream=tntsports", logo_url=None, category_id=1, is_active=True),
                Channel(name="ESPN Premium", slug="espnpremium", stream_url="https://tvtvhd.com/vivo/canales.php?stream=espnpremium", logo_url=None, category_id=1, is_active=True),
                Channel(name="TyC Sports", slug="tycsports", stream_url="https://tvtvhd.com/vivo/canales.php?stream=tycsports", logo_url=None, category_id=1, is_active=True),
                Channel(name="TyC Sports Internacional (USA)", slug="tycsportsinternacionalusa", stream_url="https://tvtvhd.com/vivo/canales.php?stream=tycsportsinternacional(usa)", logo_url=None, category_id=1, is_active=True),
                Channel(name="Telefe", slug="telefe", stream_url="https://tvtvhd.com/vivo/canales.php?stream=telefe", logo_url=None, category_id=1, is_active=True),
                Channel(name="TV Pública", slug="tvpublica", stream_url="https://tvtvhd.com/vivo/canales.php?stream=tvpública", logo_url=None, category_id=1, is_active=True),
                Channel(name="GOLPERU", slug="golperu", stream_url="https://tvtvhd.com/vivo/canales.php?stream=golperu", logo_url=None, category_id=1, is_active=True),
                Channel(name="Liga1 MAX", slug="liga1max", stream_url="https://tvtvhd.com/vivo/canales.php?stream=liga1max", logo_url=None, category_id=1, is_active=True),
                Channel(name="Movistar Deportes", slug="movistardeportes", stream_url="https://tvtvhd.com/vivo/canales.php?stream=movistardeportes", logo_url=None, category_id=1, is_active=True),
                Channel(name="Win Sports Plus", slug="winsportsplus", stream_url="https://tvtvhd.com/vivo/canales.php?stream=winsportsplus", logo_url=None, category_id=1, is_active=True),
                Channel(name="Win Sports plus (2)", slug="winsports2", stream_url="https://tvtvhd.com/vivo/canales.php?stream=winsports2", logo_url=None, category_id=1, is_active=True),
                Channel(name="Win Sports", slug="winsports", stream_url="https://tvtvhd.com/vivo/canales.php?stream=winsports", logo_url=None, category_id=1, is_active=True),
                Channel(name="Fox Sports Premium", slug="foxsportspremium", stream_url="https://tvtvhd.com/vivo/canales.php?stream=foxsportspremium", logo_url=None, category_id=1, is_active=True),
                Channel(name="TUDN", slug="tudn", stream_url="https://tvtvhd.com/vivo/canales.php?stream=tudn", logo_url=None, category_id=1, is_active=True),
                Channel(name="Caliente TV", slug="calientetv", stream_url="https://tvtvhd.com/vivo/canales.php?stream=calientetv", logo_url=None, category_id=1, is_active=True),
                Channel(name="Azteca 7", slug="azteca7", stream_url="https://tvtvhd.com/vivo/canales.php?stream=azteca7", logo_url=None, category_id=1, is_active=True),
                Channel(name="Canal 5", slug="canal5", stream_url="https://tvtvhd.com/vivo/canales.php?stream=canal5", logo_url=None, category_id=1, is_active=True),
                Channel(name="TVC Deportes", slug="tvcdeportes", stream_url="https://tvtvhd.com/vivo/canales.php?stream=tvcdeportes", logo_url=None, category_id=1, is_active=True),
                Channel(name="Azteca Deportes", slug="aztecadeportes", stream_url="https://tvtvhd.com/vivo/canales.php?stream=aztecadeportes", logo_url=None, category_id=1, is_active=True),
                Channel(name="Hisports", slug="hisports", stream_url="https://tvtvhd.com/vivo/canales.php?stream=hisports", logo_url=None, category_id=1, is_active=True),
                Channel(name="Sky Sports LaLiga", slug="skysportslaliga", stream_url="https://tvtvhd.com/vivo/canales.php?stream=skysportslaliga", logo_url=None, category_id=1, is_active=True),
                Channel(name="Sky Sports Bundesliga", slug="skysportsbundesliga", stream_url="https://tvtvhd.com/vivo/canales.php?stream=skysportsbundesliga", logo_url=None, category_id=1, is_active=True),
                Channel(name="Fox Deportes", slug="foxdeportes", stream_url="https://tvtvhd.com/vivo/canales.php?stream=foxdeportes", logo_url=None, category_id=1, is_active=True),
                Channel(name="ESPN Deportes", slug="espndeportes", stream_url="https://tvtvhd.com/vivo/canales.php?stream=espndeportes", logo_url=None, category_id=1, is_active=True),
                Channel(name="Univisión", slug="univision", stream_url="https://tvtvhd.com/vivo/canales.php?stream=univisión", logo_url=None, category_id=1, is_active=True),
                Channel(name="Fox Sports 1", slug="foxsports1", stream_url="https://tvtvhd.com/vivo/canales.php?stream=foxsports1", logo_url=None, category_id=1, is_active=True),
                Channel(name="Universo", slug="universo", stream_url="https://tvtvhd.com/vivo/canales.php?stream=universo", logo_url=None, category_id=1, is_active=True),
                Channel(name="BeIN Sports Español", slug="beinsportsespanol", stream_url="https://tvtvhd.com/vivo/canales.php?stream=beinsportsespañol", logo_url=None, category_id=1, is_active=True),
                Channel(name="Unimás", slug="unimas", stream_url="https://tvtvhd.com/vivo/canales.php?stream=unimás", logo_url=None, category_id=1, is_active=True),
                Channel(name="BeIN Sports Xtra Español", slug="beinsportsxtraespanol", stream_url="https://tvtvhd.com/vivo/canales.php?stream=beinsportsxtraespañol", logo_url=None, category_id=1, is_active=True),
                Channel(name="ESPN U", slug="espnu", stream_url="https://tvtvhd.com/vivo/canales.php?stream=espnu", logo_url=None, category_id=1, is_active=True),
                Channel(name="CBS Sports Network", slug="cbssportsnetwork", stream_url="https://tvtvhd.com/vivo/canales.php?stream=cbssportsnetwork", logo_url=None, category_id=1, is_active=True),
                Channel(name="USAnetwork", slug="usanetwork", stream_url="https://tvtvhd.com/vivo/canales.php?stream=usanetwork", logo_url=None, category_id=1, is_active=True),
                Channel(name="Telemundo", slug="telemundo", stream_url="https://tvtvhd.com/vivo/canales.php?stream=telemundo", logo_url=None, category_id=1, is_active=True),
                Channel(name="TNT Sports Chile", slug="tntsportschile", stream_url="https://tvtvhd.com/vivo/canales.php?stream=tntsportschile", logo_url=None, category_id=1, is_active=True),
                Channel(name="Premiere 1", slug="premiere1", stream_url="https://tvtvhd.com/vivo/canales.php?stream=premiere1", logo_url=None, category_id=1, is_active=True),
                Channel(name="Premiere 2", slug="premiere2", stream_url="https://tvtvhd.com/vivo/canales.php?stream=premiere2", logo_url=None, category_id=1, is_active=True),
                Channel(name="Premiere 3", slug="premiere3", stream_url="https://tvtvhd.com/vivo/canales.php?stream=premiere3", logo_url=None, category_id=1, is_active=True),
                Channel(name="Premiere 4", slug="premiere4", stream_url="https://tvtvhd.com/vivo/canales.php?stream=premiere4", logo_url=None, category_id=1, is_active=True),
                Channel(name="Premiere 5", slug="premiere5", stream_url="https://tvtvhd.com/vivo/canales.php?stream=premiere5", logo_url=None, category_id=1, is_active=True),
                Channel(name="Premiere 6", slug="premiere6", stream_url="https://tvtvhd.com/vivo/canales.php?stream=premiere6", logo_url=None, category_id=1, is_active=True),
                Channel(name="Premiere 7", slug="premiere7", stream_url="https://tvtvhd.com/vivo/canales.php?stream=premiere7", logo_url=None, category_id=1, is_active=True),
                Channel(name="Premiere 8", slug="premiere8", stream_url="https://tvtvhd.com/vivo/canales.php?stream=premiere8", logo_url=None, category_id=1, is_active=True),
                Channel(name="Sportv", slug="sportv", stream_url="https://tvtvhd.com/vivo/canales.php?stream=sportv", logo_url=None, category_id=1, is_active=True),
                Channel(name="Sportv 2", slug="sportv2", stream_url="https://tvtvhd.com/vivo/canales.php?stream=sportv2", logo_url=None, category_id=1, is_active=True),
                Channel(name="Sportv 3", slug="sportv3", stream_url="https://tvtvhd.com/vivo/canales.php?stream=sportv3", logo_url=None, category_id=1, is_active=True),
                Channel(name="Sport TV 1", slug="sporttv1", stream_url="https://tvtvhd.com/vivo/canales.php?stream=sporttv1", logo_url=None, category_id=1, is_active=True),
                Channel(name="Sport TV 2", slug="sporttv2", stream_url="https://tvtvhd.com/vivo/canales.php?stream=sporttv2", logo_url=None, category_id=1, is_active=True),
                Channel(name="Sport TV 3", slug="sporttv3", stream_url="https://tvtvhd.com/vivo/canales.php?stream=sporttv3", logo_url=None, category_id=1, is_active=True),
                Channel(name="Sport TV 4", slug="sporttv4", stream_url="https://tvtvhd.com/vivo/canales.php?stream=sporttv4", logo_url=None, category_id=1, is_active=True),
                Channel(name="Sport TV 5", slug="sporttv5", stream_url="https://tvtvhd.com/vivo/canales.php?stream=sporttv5", logo_url=None, category_id=1, is_active=True),
                Channel(name="Sport TV 6", slug="sporttv6", stream_url="https://tvtvhd.com/vivo/canales.php?stream=sporttv6", logo_url=None, category_id=1, is_active=True),
                Channel(name="Canal 11", slug="canal11", stream_url="https://tvtvhd.com/vivo/canales.php?stream=canal11", logo_url=None, category_id=1, is_active=True),
                Channel(name="Dazn Eleven 1", slug="dazneleven1", stream_url="https://tvtvhd.com/vivo/canales.php?stream=dazneleven1", logo_url=None, category_id=1, is_active=True),
                Channel(name="Dazn Eleven 2", slug="dazneleven2", stream_url="https://tvtvhd.com/vivo/canales.php?stream=dazneleven2", logo_url=None, category_id=1, is_active=True),
                Channel(name="Dazn Eleven 3", slug="dazneleven3", stream_url="https://tvtvhd.com/vivo/canales.php?stream=dazneleven3", logo_url=None, category_id=1, is_active=True),
                Channel(name="Dazn Eleven 4", slug="dazneleven4", stream_url="https://tvtvhd.com/vivo/canales.php?stream=dazneleven4", logo_url=None, category_id=1, is_active=True),
                Channel(name="Dazn Eleven 5", slug="dazneleven5", stream_url="https://tvtvhd.com/vivo/canales.php?stream=dazneleven5", logo_url=None, category_id=1, is_active=True),
                Channel(name="Dazn Eleven 6", slug="dazneleven6", stream_url="https://tvtvhd.com/vivo/canales.php?stream=dazneleven6", logo_url=None, category_id=1, is_active=True),
                Channel(name="DAZN 1", slug="dazn1", stream_url="https://tvtvhd.com/vivo/canales.php?stream=dazn1", logo_url=None, category_id=1, is_active=True),
                Channel(name="DAZN 2", slug="dazn2", stream_url="https://tvtvhd.com/vivo/canales.php?stream=dazn2", logo_url=None, category_id=1, is_active=True),
                Channel(name="DAZN 3 (eventos)", slug="dazn3eventos", stream_url="https://tvtvhd.com/vivo/canales.php?stream=dazn3(eventos)", logo_url=None, category_id=1, is_active=True),
                Channel(name="DAZN 4 (eventos)", slug="dazn4eventos", stream_url="https://tvtvhd.com/vivo/canales.php?stream=dazn4(eventos)", logo_url=None, category_id=1, is_active=True),
                Channel(name="DAZN LaLiga", slug="daznlaliga", stream_url="https://tvtvhd.com/vivo/canales.php?stream=daznlaliga", logo_url=None, category_id=1, is_active=True),
                Channel(name="La 1 TVE", slug="la1tve", stream_url="https://tvtvhd.com/vivo/canales.php?stream=la1tve", logo_url=None, category_id=1, is_active=True),
                Channel(name="Liga de Campeones 1", slug="ligadecampeones1", stream_url="https://tvtvhd.com/vivo/canales.php?stream=ligadecampeones1", logo_url=None, category_id=1, is_active=True),
                Channel(name="Liga de Campeones 2", slug="ligadecampeones2", stream_url="https://tvtvhd.com/vivo/canales.php?stream=ligadecampeones2", logo_url=None, category_id=1, is_active=True),
                Channel(name="Liga de Campeones 3", slug="ligadecampeones3", stream_url="https://tvtvhd.com/vivo/canales.php?stream=ligadecampeones3", logo_url=None, category_id=1, is_active=True),
                Channel(name="M+ LaLiga TV", slug="mpluslaligatv", stream_url="https://tvtvhd.com/vivo/canales.php?stream=mpluslaligatv", logo_url=None, category_id=1, is_active=True),
                Channel(name="LaLigaTV BAR", slug="laligatvbar", stream_url="https://tvtvhd.com/vivo/canales.php?stream=laligatvbar", logo_url=None, category_id=1, is_active=True),
                Channel(name="Sky Bundesliga 1", slug="skybundesliga1", stream_url="https://tvtvhd.com/vivo/canales.php?stream=skybundesliga1", logo_url=None, category_id=1, is_active=True),
                Channel(name="Sky Bundesliga 2", slug="skybundesliga2", stream_url="https://tvtvhd.com/vivo/canales.php?stream=skybundesliga2", logo_url=None, category_id=1, is_active=True),
                Channel(name="Sky Bundesliga 3", slug="skybundesliga3", stream_url="https://tvtvhd.com/vivo/canales.php?stream=skybundesliga3", logo_url=None, category_id=1, is_active=True),
                Channel(name="Sky Bundesliga 4", slug="skybundesliga4", stream_url="https://tvtvhd.com/vivo/canales.php?stream=skybundesliga4", logo_url=None, category_id=1, is_active=True),
                Channel(name="Sky Bundesliga 5", slug="skybundesliga5", stream_url="https://tvtvhd.com/vivo/canales.php?stream=skybundesliga5", logo_url=None, category_id=1, is_active=True),
                Channel(name="DAZN 1 DE", slug="dazn1de", stream_url="https://tvtvhd.com/vivo/canales.php?stream=dazn1de", logo_url=None, category_id=1, is_active=True),
                Channel(name="DAZN 2 DE", slug="dazn2de", stream_url="https://tvtvhd.com/vivo/canales.php?stream=dazn2de", logo_url=None, category_id=1, is_active=True),
                Channel(name="ESPN 1 NL", slug="espn1nl", stream_url="https://tvtvhd.com/vivo/canales.php?stream=espn1nl", logo_url=None, category_id=1, is_active=True),
                Channel(name="ESPN 2 NL", slug="espn2nl", stream_url="https://tvtvhd.com/vivo/canales.php?stream=espn2nl", logo_url=None, category_id=1, is_active=True),
                Channel(name="ESPN 3 NL", slug="espn3nl", stream_url="https://tvtvhd.com/vivo/canales.php?stream=espn3nl", logo_url=None, category_id=1, is_active=True),
            ]
            db.add_all(channels_data)
            db.commit()
    finally:
        db.close()

seed_db()

app = FastAPI(
    title="bustaTv API",
    description="API para la plataforma de streaming bustaTv",
    version="1.0.0",
)

# CORS para React dev server + production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # Dev server (localhost)
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5601",
        "http://127.0.0.1:5601",
        # Production (Vercel + custom domain)
        "https://local-tv-gold.vercel.app",
        "https://tv.jobustamante.dev",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(channels.router)
app.include_router(categories.router)
app.include_router(streams.router)
app.include_router(auth.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "bustaTv API v1.0"}

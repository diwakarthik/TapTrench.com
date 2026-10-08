/* =====================================================================
   TAP TRENCH — LIVE SETTINGS
   Edit this file straight on GitHub (pencil icon) — no rebuild needed.
   ===================================================================== */
window.TT = {

  /* ---------- Google Forms ----------
     In Google Forms: Send → the  < >  (embed) tab → copy ONLY the src="..." URL.
     It looks like: https://docs.google.com/forms/d/e/XXXXXXXX/viewform?embedded=true
     Leave "" and the page shows an "email us instead" button.                         */
  forms: {
    contact:  "https://docs.google.com/forms/d/e/1FAIpQLSfKthNAHmzDUIqPO019fQp1FeY0tbluP2kq6H6indL0T3vzVg/viewform?embedded=true",   // Contact Us page
    activate: "https://docs.google.com/forms/d/e/1FAIpQLSelJHY2-ykU2Tcx6N6MfOp8g4mNb7dVfue6CrZJ1WusC9VIUw/viewform?embedded=true",   // Activate Your Product page
    reseller: "https://docs.google.com/forms/d/e/1FAIpQLScsPGbOgSkFe8vy9XreZ3D2eiPoPhlGFFlsInR5eMmXDTRd3A/viewform?embedded=true",   // Become a Reseller page
    waitlist: "https://docs.google.com/forms/d/e/1FAIpQLSfNkJOBpv83-4DCIfs3AF4ynWyCVLx0c0_VzwwMpOjKveO1Tw/viewform?embedded=true"    // "Notify me" pop-up on sold-out products
  },

  /* ---------- Brand carousel ----------
     Add as many as you like (100+ is fine — they're split across two scrolling rows).
     Put logo files (SVG or transparent PNG) in  assets/logos/  and reference them here.
     If "logo" is empty the name is shown as a clean wordmark instead.
     Logo files are named after the brand (e.g. assets/logos/pizza-hut.webp), so you can see at a glance what's already there.                  */
  brands: [
    { name: "R.M. Williams",             logo: "assets/logos/rm-williams.webp" },
    { name: "Crust Pizza",               logo: "" },
    { name: "Pizza Hut",                 logo: "assets/logos/pizza-hut.webp" },
    { name: "Domino's",                  logo: "assets/logos/dominos.webp" },
    { name: "Bakers Delight",            logo: "assets/logos/bakers-delight.webp" },
    { name: "Boost Juice",               logo: "assets/logos/boost-juice.webp" },
    { name: "Subway",                    logo: "assets/logos/subway.webp" },
    { name: "Sushi Hub",                 logo: "assets/logos/sushi-hub.webp" },
    { name: "T2 Tea",                    logo: "assets/logos/t2-tea.webp" },
    { name: "Toyota",                    logo: "assets/logos/toyota.svg" },
    { name: "Kia",                       logo: "assets/logos/kia.svg" },
    { name: "Optus",                     logo: "assets/logos/optus.webp" },
    { name: "Lexus",                     logo: "assets/logos/lexus.webp" },
    { name: "Volvo",                     logo: "assets/logos/volvo.svg" },
    { name: "Jim's Group",               logo: "assets/logos/jims-group.webp" },
    { name: "Chatime",                   logo: "" },
    { name: "Gong Cha",                  logo: "assets/logos/gong-cha.webp" },
    { name: "Boeing",                    logo: "assets/logos/boeing.svg" },
    { name: "Qantas",                    logo: "assets/logos/qantas.svg" },
    { name: "Crown",                     logo: "assets/logos/crown.webp" },
    { name: "KFC",                       logo: "assets/logos/kfc.svg" },
    { name: "McDonald's",                logo: "assets/logos/mcdonalds.svg" },
    { name: "Hungry Jack's",             logo: "assets/logos/hungry-jacks.svg" },
    { name: "Papa Flock",                logo: "" },
    { name: "Lanzhou 1919 Beef Noodles", logo: "" },
    { name: "Petbarn",                   logo: "" },
    { name: "Supercheap Auto",           logo: "assets/logos/supercheap-auto.webp" },
    { name: "I Love Pizza",              logo: "" },
    { name: "Ogalo",                     logo: "" },
    { name: "Oporto",                    logo: "assets/logos/oporto.webp" },
    { name: "Ozeki",                     logo: "" },
    { name: "PappaRich",                 logo: "assets/logos/papparich.webp" },
    { name: "Anytime Fitness",           logo: "assets/logos/anytime-fitness.webp" },
    { name: "Fitness First",             logo: "assets/logos/fitness-first.webp" },
    { name: "Lamborghini",               logo: "assets/logos/lamborghini.svg" },
    { name: "Audi",                      logo: "assets/logos/audi.svg" },
    { name: "Rolls-Royce",               logo: "assets/logos/rolls-royce.svg" },
    { name: "Yo-Chi",                    logo: "assets/logos/yo-chi.webp" },
    { name: "Grill'd",                   logo: "assets/logos/grilld.webp" },
    { name: "Roll'd",                    logo: "assets/logos/rolld.webp" },
    { name: "Zeus Street Greek",         logo: "assets/logos/zeus-street-greek.webp" },
    { name: "Mad Mex",                   logo: "assets/logos/mad-mex.webp" },
    { name: "Fishbowl",                  logo: "" },
    { name: "Nene Chicken",              logo: "assets/logos/nene-chicken.webp" },
    { name: "Tesla",                     logo: "assets/logos/tesla.svg" },
    { name: "BMW",                       logo: "assets/logos/bmw.svg" },
    { name: "BYD",                       logo: "assets/logos/byd.webp" },
    { name: "Porsche",                   logo: "assets/logos/porsche.svg" },
    { name: "Mercedes-Benz",             logo: "assets/logos/mercedes-benz.webp" },
    { name: "Chery",                     logo: "assets/logos/chery.webp" },
    { name: "Guzman y Gomez",            logo: "assets/logos/guzman-y-gomez.webp" },
    { name: "Zambrero",                  logo: "assets/logos/zambrero.webp" }
  ]
};

import requests, os

urls = {
    "icar_naarm_climate_agri.pdf": "https://naarm.org.in/wp-content/uploads/2020/06/ICAR-NAARM-Policy-on-Climate-Change-and-Agriculture_compressed.pdf",
    "dst_climate_agriculture.pdf": "https://dst.gov.in/sites/default/files/Report_DST_CC_Agriculture.pdf",
    "icar_crida_vulnerability_atlas.pdf": "https://www.icar-crida.res.in/assets/img/Books/2013-14/Vulerability_Atlas_web.pdf",
    "icar_crida_vulnerability_atlas_2020.pdf": "https://www.icar-crida.res.in/assets_c/img/Books/Atlas%20climate%20change%20Aug%202020.pdf",
    "icar_naarm_adaptation_strategies.pdf": "https://eprints.cmfri.org.in/14407/1/Climate%20Change%20and%20Indian%20Agriculture%20Challenges%20and%20Adaptation%20Strategies_2020_Grinson%20George.pdf",
    "nabard_risk_mgmt_agri.pdf": "https://www.nabard.org/auth/writereaddata/tender/2007223845Paper-4-Climate-and-Risk-Management-Dr.-Birthal.pdf",
    "ipcc_ar6_synthesis_report.pdf": "https://www.ipcc.ch/site/assets/uploads/2023/03/Doc5_Adopted_AR6_SYR_Longer_Report.pdf"
}

os.makedirs("data/knowledge_base", exist_ok=True)

for name, url in urls.items():
    print(f"Downloading {name}...")
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    with open(os.path.join("data/knowledge_base", name), "wb") as f:
        f.write(r.content)
print("✅ All files downloaded successfully!")
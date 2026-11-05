# 🏛️ debim Benchmark Example 2: แบบบ้านครอบครัวไทยร่วมสมัย 5 (Modular Architecture)

[![debim Model Validation & Test Suite](https://github.com/PRIDA-TAKON/example2-debim/actions/workflows/ci.yml/badge.svg)](https://github.com/PRIDA-TAKON/example2-debim/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![IFC4 Certified](https://img.shields.io/badge/IFC4-Minimal%203D%20Solid-green.svg)](family5_model.ifc)
[![Certified BOQ Match](https://img.shields.io/badge/Certified%20BOQ-100%25%20Exact%20Match-brightgreen.svg)](#-certified-boq-audit--deterministic-qto)

โมเดลอาคารตัวอย่างแบบแยกโมดูลย่อย (**Modular Declarative BIM / Building-as-Code**) สำหรับ **แบบบ้านครอบครัวไทยร่วมสมัย 5 (family5.pdf)** แหล่งที่มาแบบมาตรฐานจาก **กรมโยธาธิการและผังเมือง กระทรวงมหาดไทย** 

โปรเจกต์นี้แสดงการออกแบบสถาปัตยกรรมและวิศวกรรมอาคาร 2 ชั้น พร้อมโครงสร้างคานยื่น (Cantilevered Structure), Bay Window, โถงบันไดยื่นพ้นแนวเสา, โครงสร้างหลังคาเพิงหมาแหงน และงานระบบ MEP ครบวงจร โดยเชื่อมโยงและผ่านการตรวจสอบปริมาณวัสดุและการก่อสร้างจริงตาม **BOQ (ปร.4) 100.0% Exact Match (129/129 รายการ)**

---

## 🌟 จุดเด่นของโปรเจกต์ (Key Architectural & Engineering Features)

1. **สถาปัตยกรรมแบบแยกหลายไฟล์ (Modular debim Architecture):**
   - แตกไฟล์ Monolithic ขนาดใหญ่ ออกเป็นโมดูลย่อย 18 ไฟล์ตามหมวดงานวิศวกรรมและสถาปัตยกรรม ทำให้ทำงานร่วมกันผ่าน Git ได้ง่าย ไร้ Merge Conflicts และปรับแก้งานได้เป็นสัดส่วน
   - เชื่อมโยงผ่าน Root Manifest `project.debim` (หรือ `project.yaml`) ด้วยคำสั่ง `includes: models/**/*.yaml`
2. **รูปทรงเรขาคณิตตรงตามแบบจริง 100% (True Cantilever Geometry):**
   - **Bay Window ห้องพักผ่อนชั้น 1:** ยื่นพ้นแนวเสากริด 1 ออกไปทางทิศตะวันตก `-0.60 ม.` พร้อมคานยื่น `GB-CANT-1B/1C/EDGE` และหน้าต่าง `WIN-N1-LIVING`
   - **ชั้น 2 ทิศตะวันตก (Master Bed, ห้องน้ำ 2, ห้องนอน 3):** ยื่นพ้นแนวเสากริด 1 ออกไป `-0.60 ม.` (พิกัด X = -0.60 ม.) พร้อมคานยื่น `B-CANT-1B..1E/EDGE`
   - **ผนังหน้าห้องนอนใหญ่ ชั้น 2:** ยื่นออกไปทางทิศใต้สู่แนวระเบียง `-0.70 ม.` (พิกัด Y = B - 0.70 ม.) พร้อมคานยื่น `B-CANT-FRONT-1/2/EDGE`
   - **โถงบันไดและชานพักยื่น (Cantilever Staircase):** ยื่นพ้นแนวเสากริด 4 ออกไปทางทิศตะวันออก `+0.50 ม.` (พิกัด X = 9.00 ถึง 9.50 ม.) พร้อมคานยื่น `GB-CANT-STAIR-4C/4D`, `B-CANT-STAIR-4C/4D`, ชานพัก `STAIR-LANDING`, และหน้าต่างกระจกสูงโถงบันได `WIN-N5-STAIR`
   - **ครัวไทยด้านหลัง:** ต่อขยายออกไปถึงแนวกริด F ครบถ้วน
3. **ระบบทดสอบครอบคลุม (Comprehensive Automated Test Suite):**
   - มีชุดทดสอบด้วย `pytest` ครอบคลุม Schema, Topology, Collision/Clash Detection, การคอมไพล์ IFC4, มิติของ Cantilever, และความตรงเป๊ะของ BOQ รวม 14 การทดสอบ (Passed 100%)

---

## 📁 โครงสร้างโปรเจกต์ (Modular File Structure)

```text
example2-debim/
├── project.debim                     # Root BIM Manifest (debim format)
├── project.yaml                      # Root BIM Manifest (YAML format with includes)
├── family5_model.ifc                 # Compiled IFC4 Standard Model (521 KB)
├── index.html                        # Standalone 3D Interactive Web Viewer
├── LICENSE                           # Open-Source MIT License
├── .gitignore
├── .github/
│   └── workflows/
│       └── ci.yml                    # Automated GitHub Actions CI Testing Workflow
├── tests/                            # Automated Pytest Test Suite
│   ├── test_validation.py            # Schema, Topology Continuity & Spatial Hierarchy
│   ├── test_compilation.py           # IFC4 Compilation & Entity Integrity Tests
│   ├── test_cantilevers_and_stairs.py# Geometry verification for Cantilevers & Staircase
│   └── test_boq_qto.py               # Deterministic QTO vs Certified BOQ Match Tests
└── models/                           # Modular BIM Components (18 Modular Sub-Files)
    ├── architecture/                 # สถาปัตยกรรม
    │   ├── spaces.yaml               # ขอบเขตห้องและพื้นที่อาคาร (Spaces & Massing)
    │   ├── walls.yaml                # ผนังก่ออิฐมอญครึ่งแผ่นและเต็มแผ่นพร้อมส่วนยื่น
    │   ├── doors_windows.yaml        # ประตู D1-D4 และหน้าต่าง W1-W5
    │   ├── finishes.yaml             # งานฉาบปูน ปูกระเบื้อง บัวเชิงผนัง
    │   ├── roofs.yaml                # แผ่นหลังคาเหล็กรีดลอนและแผ่นครอบ
    │   └── insulation.yaml           # ฉนวนกันความร้อนใต้หลังคา
    ├── structure/                    # วิศวกรรมโครงสร้าง
    │   ├── foundations.yaml          # เสาเข็มหกเหลี่ยม 157 ต้น ฐานราก และตอม่อ
    │   ├── columns.yaml              # เสา ค.ส.ล. ชั้น 1 และ ชั้น 2
    │   ├── beams.yaml                # คานคอดิน คานชั้นสอง และคานยื่น Cantilever
    │   ├── slabs.yaml                # พื้น ค.ส.ล. หล่อในที่, แผ่นพื้นสำเร็จ และชานพักบันได
    │   └── members.yaml              # โครงหลังคาเหล็ก แป จันทัน เชิงชาย และราวกั้น
    └── mep/                          # วิศวกรรมระบบอาคาร (MEP)
        ├── cold_water.yaml           # ท่อน้ำดีและมิเตอร์น้ำ
        ├── fixtures.yaml             # สุขภัณฑ์ โถสุขภัณฑ์ อ่างล้างหน้า ฝักบัว
        ├── terminals.yaml            # ท่อน้ำทิ้ง ท่อโสโครก ท่อระบายอากาศ
        ├── equipment.yaml            # ถังบำบัดน้ำเสีย ถังดักไขมัน ถังน้ำ ปั๊มน้ำ
        ├── panels.yaml               # ตู้ควบคุมไฟฟ้าหลัก (Main DB Consumer Unit)
        ├── lighting.yaml             # ดวงโคมดาวน์ไลท์ ฟลูออเรสเซนต์ ไฟกิ่ง
        └── power.yaml                # สวิตช์ เต้ารับ สายไฟ ท่อร้อยสาย และระบบสายดิน
```

---

## 🚀 วิธีการใช้งาน (Getting Started)

### 1. การติดตั้งเครื่องมือ
ต้องการ Python 3.10+ และติดตั้ง `debim` CLI:
```bash
pip install debim pytest pyyaml
```

### 2. ตรวจสอบความถูกต้องของโมเดล (Validation)
ตรวจสอบ Schema, ความต่อเนื่องทางโครงสร้าง (Topological Continuity), และการชนกันของระบบ (Clash Detection):
```bash
debim validate -m project.yaml
```

### 3. คอมไพล์เป็นโมเดลมาตรฐาน IFC4 (Compilation)
แปลงโค้ด Declarative BIM เป็นไฟล์มาตรฐานเปิด IFC4 Solid Geometry:
```bash
debim compile -m project.yaml -o family5_model.ifc
```

### 4. เปิดดูโมเดล 3 มิติ (3D Web Viewer)
เปิดดูโมเดล 3 มิติแบบ Interactive ผ่านเว็บเบราว์เซอร์:
```bash
# เปิด Interactive Server
debim view -m project.yaml

# หรือเปิดดูไฟล์ standalone index.html โดยตรง
open index.html
```

### 5. คำนวณปริมาณงานก่อสร้าง (QTO & BOQ)
```bash
debim qto -m project.yaml
debim boq -m project.yaml
```

### 6. การรันชุดทดสอบอัตโนมัติ (Automated Tests)
```bash
python -m pytest tests/ -v
```

---

## 📊 ผลการตรวจสอบความสอดคล้อง BOQ (Certified Audit Summary)

โมเดลนี้ผ่านการทดสอบและ Audit เทียบกับเอกสารประมาณราคาทางการ **BOQ (ปร.4)** กรมโยธาธิการและผังเมือง กระทรวงมหาดไทย:

| หมวดงานก่อสร้าง | รายการตรวจสอบหลัก | ปริมาณ BOQ | ปริมาณ debim QTO | ผลการตรวจ |
| :--- | :--- | :---: | :---: | :---: |
| **งานฐานราก** | เสาเข็มหกเหลี่ยมกลวง Ø 0.15 ม. ยาว 6.00 ม. | 157 ต้น | 157 ต้น | **100% Exact** |
| **งานคอนกรีต** | คอนกรีตฐานรากและตอม่อ | 23.00 ลบ.ม. | 23.00 ลบ.ม. | **100% Exact** |
| **งานแผ่นพื้น** | แผ่นพื้นสำเร็จรูปท้องเรียบ หนา 5 ซม. | 149.00 ตร.ม. | 149.00 ตร.ม. | **100% Exact** |
| **งานโครงสร้างเหล็ก** | เหล็กโครงหลังคา (C100, C125, แผ่นเหล็ก) | 1,533.00 กก. | 1,533.00 กก. | **100% Exact** |
| **งานก่ออิฐ** | ผนังก่ออิฐมอญครึ่งแผ่น | 308.00 ตร.ม. | 308.00 ตร.ม. | **100% Exact** |
| **งานก่ออิฐ** | ผนังก่ออิฐมอญเต็มแผ่น | 47.00 ตร.ม. | 47.00 ตร.ม. | **100% Exact** |
| **งานประตู-หน้าต่าง** | บานประตู-หน้าต่างรวมทุกประเภท | 29 ชุด | 29 ชุด | **100% Exact** |
| **งานไฟฟ้า** | ดวงโคมส่องสว่าง (ดาวน์ไลท์, ฟลูฯ, ไฟกิ่ง) | 41 ชุด | 41 ชุด | **100% Exact** |
| **งานไฟฟ้า** | สวิตช์ควบคุมวงจรไฟฟ้า | 22 ชุด | 22 ชุด | **100% Exact** |
| **งานไฟฟ้า** | เต้ารับไฟฟ้าคู่มีกราวด์ | 21 ชุด | 21 ชุด | **100% Exact** |

> **ผลรวมการ Audit ทั้งหมด:** ผ่านการตรวจสอบตรงกันทุกประการ **129 จาก 129 รายการ (100.0% Exact Match)**

---

## 📜 ลิขสิทธิ์ (License)

โปรเจกต์นี้เผยแพร่ภายใต้สัญญาอนุญาต [MIT License](LICENSE) สามารถนำไปศึกษา ใช้งาน และพัฒนาต่อยอดได้อย่างเสรี

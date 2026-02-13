---
hide:
  - toc
---

# Student Ranking

<style>
.podium-card {
  transition: transform 0.35s cubic-bezier(0.4, 0, 0.2, 1),
              box-shadow 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: default;
}
.podium-card:hover {
  transform: translateY(-10px) scale(1.04);
}
.podium-gold:hover {
  box-shadow: 0 0 50px rgba(249,212,35,0.55), 0 10px 30px rgba(0,0,0,0.4) !important;
}
.podium-silver:hover {
  box-shadow: 0 0 50px rgba(168,180,194,0.45), 0 10px 30px rgba(0,0,0,0.4) !important;
}
.podium-bronze:hover {
  box-shadow: 0 0 50px rgba(205,127,50,0.45), 0 10px 30px rgba(0,0,0,0.4) !important;
}
.podium-card img {
  transition: transform 0.35s cubic-bezier(0.4, 0, 0.2, 1),
              box-shadow 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}
.podium-card:hover img {
  transform: scale(1.12);
}
.podium-gold:hover img {
  box-shadow: 0 0 30px rgba(249,212,35,0.7) !important;
}
.podium-silver:hover img {
  box-shadow: 0 0 30px rgba(168,180,194,0.6) !important;
}
.podium-bronze:hover img {
  box-shadow: 0 0 30px rgba(205,127,50,0.6) !important;
}
.podium-card .fork-btn {
  transition: background 0.3s ease, transform 0.3s ease;
}
.podium-card:hover .fork-btn {
  transform: scale(1.05);
}
.stat-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.3);
}
.logo-glow-wrap {
  display: inline-block;
  position: relative;
  margin-bottom: 12px;
}
.logo-glow-wrap img {
  display: block;
  width: 200px;
  height: auto;
  border-radius: 15px;
}
/* SVG ECG - linea de vida bajo el logo */
.ecg-svg {
  position: absolute;
  bottom: -4px;
  left: -5px;
  width: calc(100% + 10px);
  height: 32px;
  z-index: 2;
  pointer-events: none;
}
</style>

<div style="text-align: center; padding: 10px 0;">
<div class="logo-glow-wrap"><img src="../../assets/todoeconometria_logo.png" alt="TodoEconometria"><svg class="ecg-svg" viewBox="-5 -2 210 32"><defs><filter id="ecg-glow"><feGaussianBlur stdDeviation="3" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter><linearGradient id="ecg-colors" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="200" y2="0"><stop offset="0%" stop-color="#a51d4e"/><stop offset="20%" stop-color="#e63946"/><stop offset="40%" stop-color="#f4a233"/><stop offset="60%" stop-color="#2d8a56"/><stop offset="80%" stop-color="#3470bc"/><stop offset="100%" stop-color="#a51d4e"/></linearGradient></defs><path d="M -200,20 H -50 l 5,-3 l 5,3 l 5,0 l 2,3 l 2,-18 l 2,20 l 2,-5 l 5,0 l 4,-4 l 5,4 H 0 H 150 l 5,-3 l 5,3 l 5,0 l 2,3 l 2,-18 l 2,20 l 2,-5 l 5,0 l 4,-4 l 5,4 H 200 H 350 l 5,-3 l 5,3 l 5,0 l 2,3 l 2,-18 l 2,20 l 2,-5 l 5,0 l 4,-4 l 5,4 H 400" fill="none" stroke="url(#ecg-colors)" stroke-width="3" stroke-linecap="round" filter="url(#ecg-glow)" stroke-dasharray="90 642"><animate attributeName="stroke-dashoffset" from="0" to="-732" dur="3s" repeatCount="indefinite"/></path></svg></div>
<p style="font-size: 1.1em; font-style: italic; color: #888;">
Big Data with Python course leaderboard
</p>
<p style="color: #666; font-size: 0.9em;">
Last updated: 2026-02-13 01:53 | Automatic course evaluation
</p>
</div>

---

<h2 style="border: none;">Course Statistics</h2>

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin: 30px 0; text-align: center;">
<div class="stat-card" style="background: linear-gradient(180deg, #1a1a2e, #16213e); border-radius: 12px; padding: 20px; border: 1px solid rgba(255,255,255,0.05);"><div style="font-size: 2.5em; font-weight: 900; color: #f39c12; text-shadow: 0 0 20px rgba(243,156,18,0.3);">18</div><div style="color: #888; font-size: 0.9em; margin-top: 4px;">Students</div></div><div class="stat-card" style="background: linear-gradient(180deg, #1a1a2e, #16213e); border-radius: 12px; padding: 20px; border: 1px solid rgba(255,255,255,0.05);"><div style="font-size: 2.5em; font-weight: 900; color: #2ecc71; text-shadow: 0 0 20px rgba(46,204,113,0.3);">3</div><div style="color: #888; font-size: 0.9em; margin-top: 4px;">Delivered</div></div><div class="stat-card" style="background: linear-gradient(180deg, #1a1a2e, #16213e); border-radius: 12px; padding: 20px; border: 1px solid rgba(255,255,255,0.05);"><div style="font-size: 2.5em; font-weight: 900; color: #3498db; text-shadow: 0 0 20px rgba(52,152,219,0.3);">8.0</div><div style="color: #888; font-size: 0.9em; margin-top: 4px;">Average</div></div><div class="stat-card" style="background: linear-gradient(180deg, #1a1a2e, #16213e); border-radius: 12px; padding: 20px; border: 1px solid rgba(255,255,255,0.05);"><div style="font-size: 2.5em; font-weight: 900; color: #e74c3c; text-shadow: 0 0 20px rgba(231,76,60,0.3);">2</div><div style="color: #888; font-size: 0.9em; margin-top: 4px;">Outstanding</div></div>
</div>

---

<h2 style="border: none;">Leaderboard</h2>

<div style="display: grid; grid-template-columns: 1fr 1.2fr 1fr; gap: 14px; margin: 30px auto; max-width: 820px; align-items: end;">
<div class="podium-card podium-silver" style="min-height: 300px; background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f0f23 100%); border-radius: 16px; padding: 22px 14px 18px; border: 1px solid #a8b4c240; box-shadow: 0 0 25px rgba(168,180,194,0.2), 0 4px 15px rgba(0,0,0,0.3); display: flex; flex-direction: column; align-items: center; position: relative; overflow: hidden;"><div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, transparent, #a8b4c2, transparent);"></div><div style="font-size: 1.6em; font-weight: 900; color: #c0c0c0; text-shadow: 0 0 15px rgba(168,180,194,0.2); margin-bottom: 10px; letter-spacing: 2px;">#2</div><img src="https://github.com/aurorafezu.png" alt="@aurorafezu" style="width: 72px; height: 72px; border-radius: 50%; border: 3px solid #a8b4c2; box-shadow: 0 0 15px rgba(168,180,194,0.2); object-fit: cover; background: #2a2a3a;" onerror="this.style.display='none'"><div style="margin-top: 10px; font-weight: 700; color: #eee; font-size: 0.95em;">@aurorafezu</div><div style="font-size: 2em; font-weight: 900; color: #c0c0c0; text-shadow: 0 0 10px rgba(168,180,194,0.2); margin: 4px 0; letter-spacing: 1px;">8.2</div><div style="width: 90%; margin: 10px 0 6px;"><div style="display: flex; align-items: center; gap: 5px; margin: 4px 0;"><span style="width: 30px; font-weight: 800; color: #e8b84b; font-size: 0.65em;">Doc</span><div style="flex: 1; background: #2a2a3a; border-radius: 4px; height: 7px; overflow: hidden;"><div style="width: 70%; background: linear-gradient(90deg, #e8b84b, #f9d423); height: 100%; border-radius: 4px;"></div></div><span style="font-size: 0.7em; color: #999; width: 28px; text-align: right;">7.0</span></div><div style="display: flex; align-items: center; gap: 5px; margin: 4px 0;"><span style="width: 30px; font-weight: 800; color: #667eea; font-size: 0.65em;">Code</span><div style="flex: 1; background: #2a2a3a; border-radius: 4px; height: 7px; overflow: hidden;"><div style="width: 100%; background: linear-gradient(90deg, #667eea, #764ba2); height: 100%; border-radius: 4px;"></div></div><span style="font-size: 0.7em; color: #999; width: 28px; text-align: right;">10.0</span></div></div><div style="margin: 6px 0 4px; line-height: 1.8;"><span style="display: inline-block; background: rgba(102,126,234,0.12); border: 1px solid rgba(102,126,234,0.25); border-radius: 10px; padding: 1px 9px; font-size: 0.68em; color: #8b9cf7; margin: 1px 2px;">clustering</span><span style="display: inline-block; background: rgba(102,126,234,0.12); border: 1px solid rgba(102,126,234,0.25); border-radius: 10px; padding: 1px 9px; font-size: 0.68em; color: #8b9cf7; margin: 1px 2px;">k-means</span></div><a class="fork-btn" href="https://github.com/aurorafezu/ejercicios-bigdata/tree/main/entregas/trabajo_final/fernandez_aurora" target="_blank" style="color: #c0c0c0; text-decoration: none; font-size: 0.8em; margin-top: auto; padding: 5px 18px; border: 1px solid #a8b4c250; border-radius: 20px; background: #a8b4c210;">See Submission</a></div><div class="podium-card podium-gold" style="min-height: 360px; background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f0f23 100%); border-radius: 16px; padding: 22px 14px 18px; border: 1px solid #f9d42340; box-shadow: 0 0 25px rgba(249,212,35,0.3), 0 4px 15px rgba(0,0,0,0.3); display: flex; flex-direction: column; align-items: center; position: relative; overflow: hidden;"><div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, transparent, #f9d423, transparent);"></div><div style="font-size: 1.6em; font-weight: 900; color: #f9d423; text-shadow: 0 0 15px rgba(249,212,35,0.3); margin-bottom: 10px; letter-spacing: 2px;">#1</div><img src="https://github.com/katitto.png" alt="@katitto" style="width: 90px; height: 90px; border-radius: 50%; border: 3px solid #f9d423; box-shadow: 0 0 15px rgba(249,212,35,0.3); object-fit: cover; background: #2a2a3a;" onerror="this.style.display='none'"><div style="margin-top: 10px; font-weight: 700; color: #eee; font-size: 0.95em;">@katitto</div><div style="font-size: 2.6em; font-weight: 900; color: #f9d423; text-shadow: 0 0 10px rgba(249,212,35,0.3); margin: 4px 0; letter-spacing: 1px;">8.7</div><div style="width: 90%; margin: 10px 0 6px;"><div style="display: flex; align-items: center; gap: 5px; margin: 4px 0;"><span style="width: 30px; font-weight: 800; color: #e8b84b; font-size: 0.65em;">Doc</span><div style="flex: 1; background: #2a2a3a; border-radius: 4px; height: 7px; overflow: hidden;"><div style="width: 95%; background: linear-gradient(90deg, #e8b84b, #f9d423); height: 100%; border-radius: 4px;"></div></div><span style="font-size: 0.7em; color: #999; width: 28px; text-align: right;">9.5</span></div><div style="display: flex; align-items: center; gap: 5px; margin: 4px 0;"><span style="width: 30px; font-weight: 800; color: #667eea; font-size: 0.65em;">Code</span><div style="flex: 1; background: #2a2a3a; border-radius: 4px; height: 7px; overflow: hidden;"><div style="width: 100%; background: linear-gradient(90deg, #667eea, #764ba2); height: 100%; border-radius: 4px;"></div></div><span style="font-size: 0.7em; color: #999; width: 28px; text-align: right;">10.0</span></div></div><div style="margin: 6px 0 4px; line-height: 1.8;"><span style="display: inline-block; background: rgba(102,126,234,0.12); border: 1px solid rgba(102,126,234,0.25); border-radius: 10px; padding: 1px 9px; font-size: 0.68em; color: #8b9cf7; margin: 1px 2px;">pca</span><span style="display: inline-block; background: rgba(102,126,234,0.12); border: 1px solid rgba(102,126,234,0.25); border-radius: 10px; padding: 1px 9px; font-size: 0.68em; color: #8b9cf7; margin: 1px 2px;">time series</span></div><a class="fork-btn" href="https://github.com/katitto/ejercicios-bigdata/tree/main/entregas/trabajo_final/almache_katherine" target="_blank" style="color: #f9d423; text-decoration: none; font-size: 0.8em; margin-top: auto; padding: 5px 18px; border: 1px solid #f9d42350; border-radius: 20px; background: #f9d42310;">See Submission</a></div><div class="podium-card podium-bronze" style="min-height: 280px; background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f0f23 100%); border-radius: 16px; padding: 22px 14px 18px; border: 1px solid #cd7f3240; box-shadow: 0 0 25px rgba(205,127,50,0.2), 0 4px 15px rgba(0,0,0,0.3); display: flex; flex-direction: column; align-items: center; position: relative; overflow: hidden;"><div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, transparent, #cd7f32, transparent);"></div><div style="font-size: 1.6em; font-weight: 900; color: #cd7f32; text-shadow: 0 0 15px rgba(205,127,50,0.2); margin-bottom: 10px; letter-spacing: 2px;">#3</div><img src="https://github.com/luuuuru.png" alt="@luuuuru" style="width: 72px; height: 72px; border-radius: 50%; border: 3px solid #cd7f32; box-shadow: 0 0 15px rgba(205,127,50,0.2); object-fit: cover; background: #2a2a3a;" onerror="this.style.display='none'"><div style="margin-top: 10px; font-weight: 700; color: #eee; font-size: 0.95em;">@luuuuru</div><div style="font-size: 2em; font-weight: 900; color: #cd7f32; text-shadow: 0 0 10px rgba(205,127,50,0.2); margin: 4px 0; letter-spacing: 1px;">7.0</div><div style="width: 90%; margin: 10px 0 6px;"><div style="display: flex; align-items: center; gap: 5px; margin: 4px 0;"><span style="width: 30px; font-weight: 800; color: #e8b84b; font-size: 0.65em;">Doc</span><div style="flex: 1; background: #2a2a3a; border-radius: 4px; height: 7px; overflow: hidden;"><div style="width: 0%; background: linear-gradient(90deg, #e8b84b, #f9d423); height: 100%; border-radius: 4px;"></div></div><span style="font-size: 0.7em; color: #999; width: 28px; text-align: right;">0.0</span></div><div style="display: flex; align-items: center; gap: 5px; margin: 4px 0;"><span style="width: 30px; font-weight: 800; color: #667eea; font-size: 0.65em;">Code</span><div style="flex: 1; background: #2a2a3a; border-radius: 4px; height: 7px; overflow: hidden;"><div style="width: 100%; background: linear-gradient(90deg, #667eea, #764ba2); height: 100%; border-radius: 4px;"></div></div><span style="font-size: 0.7em; color: #999; width: 28px; text-align: right;">10.0</span></div></div><a class="fork-btn" href="https://github.com/luuuuru/ejercicios-bigdata/tree/main/entregas/trabajo_final/camacho-lucia" target="_blank" style="color: #cd7f32; text-decoration: none; font-size: 0.8em; margin-top: auto; padding: 5px 18px; border: 1px solid #cd7f3250; border-radius: 20px; background: #cd7f3210;">See Submission</a></div>
</div>


---

<h2 style="border: none;">Full Ranking</h2>


| Pos | Student | Grade | Status | Project | Fork |
|:---:|:-----------|:----:|:------:|:---------|:----:|
| **#1** | @katitto | **8.7** | &#11088; Outstanding | `almache_katherine` | [See](https://github.com/katitto/ejercicios-bigdata/tree/main/entregas/trabajo_final/almache_katherine){target="_blank"} |
| **#2** | @aurorafezu | **8.2** | &#11088; Outstanding | `fernandez_aurora` | [See](https://github.com/aurorafezu/ejercicios-bigdata/tree/main/entregas/trabajo_final/fernandez_aurora){target="_blank"} |
| **#3** | @luuuuru | **7.0** | &#9989; Approved | `camacho-lucia` | [See](https://github.com/luuuuru/ejercicios-bigdata/tree/main/entregas/trabajo_final/camacho-lucia){target="_blank"} |


---

<h2 style="border: none;">Grade Distribution</h2>

<div style="margin: 20px 0;">
<div style="display: flex; align-items: center; margin: 8px 0;"><span style="width: 130px; font-weight: bold; color: #ccc;">9-10 Excellent</span><div style="flex: 1; background: #333; border-radius: 5px; height: 28px; overflow: hidden;"><div style="width: 0%; background: linear-gradient(90deg, #f9d423, #ff4e50); height: 100%; border-radius: 5px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; min-width: 0px;"></div></div></div><div style="display: flex; align-items: center; margin: 8px 0;"><span style="width: 130px; font-weight: bold; color: #ccc;">7-8 Good</span><div style="flex: 1; background: #333; border-radius: 5px; height: 28px; overflow: hidden;"><div style="width: 100%; background: linear-gradient(90deg, #667eea, #764ba2); height: 100%; border-radius: 5px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; min-width: 35px;">3</div></div></div><div style="display: flex; align-items: center; margin: 8px 0;"><span style="width: 130px; font-weight: bold; color: #ccc;">5-6 Passing</span><div style="flex: 1; background: #333; border-radius: 5px; height: 28px; overflow: hidden;"><div style="width: 0%; background: linear-gradient(90deg, #43e97b, #38f9d7); height: 100%; border-radius: 5px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; min-width: 0px;"></div></div></div><div style="display: flex; align-items: center; margin: 8px 0;"><span style="width: 130px; font-weight: bold; color: #ccc;"><5 Below</span><div style="flex: 1; background: #333; border-radius: 5px; height: 28px; overflow: hidden;"><div style="width: 0%; background: linear-gradient(90deg, #fa709a, #fee140); height: 100%; border-radius: 5px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; min-width: 0px;"></div></div></div></div>


---

<p style="text-align: center; color: #555; font-size: 0.85em; margin-top: 40px;">
The ranking updates automatically with each evaluation. Submit your work to appear!<br>
<em>Generated by: evaluar v3.0 | 2026-02-13 01:53</em>
</p>

---

**Course:** Big Data with Python - From Zero to Production
**Professor:** Juan Marcelo Gutierrez Miranda | @TodoEconometria
**Hash ID:** 4e8d9b1a5f6e7c3d2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c
**Methodology:** Progressive exercises with real data and professional tools

**Academic references:**
- Downey, A. (2015). *Think Python: How to Think Like a Computer Scientist*. O'Reilly Media.
- McKinney, W. (2022). *Python for Data Analysis*, 3rd Ed. O'Reilly Media.
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly Media.

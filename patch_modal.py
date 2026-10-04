with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'r') as f:
    content = f.read()

old_modal = """    {isCalibrating && !isPreviewMode && (
          <div className="absolute inset-0 pointer-events-none z-20 flex flex-col items-center justify-center">
             <div className="mt-4 px-6 py-4 rounded-xl font-mono text-sm text-center bg-[#140b00]/90 text-amber-500 border border-amber-600/50 backdrop-blur-md shadow-2xl">
               <div className="font-bold text-amber-400 mb-1">Scale Calibration Mode</div>
               Measure the physical projection on the build plate.<br/>
               Adjust scale until the digital grid matches the real printer edges.
               <div className="mt-4 flex items-center gap-3 pointer-events-auto bg-[#0a0500] p-3 rounded-lg border border-[#4a2800]">
                 <input 
                   type="range" min="0.1" max="10" step="0.001" 
                   value={projScale} 
                   onChange={e => setProjScale(parseFloat(e.target.value))} 
                   className="flex-1 accent-amber-500"
                 />
                 <span className="font-bold text-amber-300 bg-[#2a1700] px-2 py-1 rounded border border-[#4a2800]">{projScale.toFixed(3)}x</span>
               </div>
             </div>
          </div>
        )}"""

new_modal = """    {isCalibrating && !isPreviewMode && (
          <div className="absolute inset-0 pointer-events-none z-20 flex flex-col items-center justify-center">
             <div className="relative mt-4 px-6 py-4 rounded-xl font-mono text-sm text-center bg-[#140b00]/90 text-amber-500 border border-amber-600/50 backdrop-blur-md shadow-2xl pointer-events-auto">
               <button 
                 onClick={() => setIsCalibrating(false)} 
                 className="absolute top-2 right-2 text-amber-600 hover:text-amber-400 font-sans font-bold px-2 py-1"
                 title="Close Calibration"
               >✕</button>
               <div className="font-bold text-amber-400 mb-1 pr-6">Scale Calibration Mode</div>
               Measure the physical projection on the build plate.<br/>
               Adjust scale until the digital grid matches the real printer edges.
               <div className="mt-4 flex items-center gap-3 bg-[#0a0500] p-3 rounded-lg border border-[#4a2800]">
                 <input 
                   type="range" min="0.1" max="10" step="0.001" 
                   value={projScale} 
                   onChange={e => setProjScale(parseFloat(e.target.value))} 
                   className="flex-1 accent-amber-500"
                 />
                 <span className="font-bold text-amber-300 bg-[#2a1700] px-2 py-1 rounded border border-[#4a2800]">{projScale.toFixed(3)}x</span>
               </div>
             </div>
          </div>
        )}"""

# Note: Added pointer-events-auto to the modal container and relative positioning for the close button.

if old_modal in content:
    content = content.replace(old_modal, new_modal)
    with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'w') as f:
        f.write(content)
else:
    print("Could not find the old modal string!")


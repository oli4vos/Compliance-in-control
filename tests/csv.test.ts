import { describe,expect,it } from "vitest";
describe("CSV-conventie",()=>{it("escapet dubbele aanhalingstekens en gebruikt Nederlandse scheiding",()=>{const csv=(v:string)=>`"${v.replaceAll('"','""')}"`;expect(["E-001",'Eis met "citaat"'].map(csv).join(";")).toBe('"E-001";"Eis met ""citaat"""')})});


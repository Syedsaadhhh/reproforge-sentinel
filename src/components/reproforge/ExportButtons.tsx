import { Button } from "@/components/ui/button";
import { Download, Share2, FileText } from "lucide-react";
import { toast } from "sonner";
import type { Passport } from "@/data/mockPassport";

export function ExportButtons({ passport }: { passport: Passport }) {
  const downloadJson = () => {
    const blob = new Blob([JSON.stringify(passport, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${passport.passport_id}.json`;
    a.click();
    URL.revokeObjectURL(url);
    toast.success("Passport JSON downloaded");
  };

  const exportPdf = () => {
    window.print();
    toast.success("Print dialog opened — choose Save as PDF");
  };

  const share = async () => {
    const url = new URL(window.location.href);
    url.searchParams.set("run_id", passport.run_id);
    await navigator.clipboard.writeText(url.toString());
    toast.success("Passport link copied");
  };

  return (
    <div className="flex flex-wrap gap-2">
      <Button onClick={downloadJson} className="gap-2">
        <Download className="h-4 w-4" /> Download JSON
      </Button>
      <Button variant="outline" className="gap-2" onClick={exportPdf}>
        <FileText className="h-4 w-4" /> Export PDF
      </Button>
      <Button variant="outline" className="gap-2" onClick={share}>
        <Share2 className="h-4 w-4" /> Share
      </Button>
    </div>
  );
}

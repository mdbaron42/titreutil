# TitreUtil
Small utility to calculate virus and antibody titres

### Purpose
This application is for anyone who either:   
(a) determines virus titre by limiting dilution on 96-well plates, i.e. they are calclating the 50% Tissue Culture Infectious Dose (TCID50)   
or   
(b) determines the titre of virus-neutralising antibodies in serum (VNT or SNT)

A common method of calculating either of these is by the formula usually ascribed to "Spearman and Kärber". I was doing these calculations a lot, so I wrote a small utility to make it easier for me and my group.

### How it works
The application has two tabs, one for virus titres (Titre Calc) and one for serum antibody titres (VNT Calc). The required parameters are entered into boxes in the application window, then you press the Calculate button (or hit the Return key) and the answer appears. If you are doing this kind of assay in the lab, you should know what the parameters are but, for clarity, for the Virus titre tab (Titre Calc):   
Plate dilution factor: fold difference between one row and the next (defaults to 10)   
Microlitres of virus per well: Included on the virus titre tab so that I can calculate the titre per ml   
Baseline dilution: the greatest dilution (lowest concentration) of virus where all the wells are infected   
Sum of proportions: the sum of the proportions (fractions) of the wells that are infected, starting at the baseline dilution and going down. Since by definition the proportion on the baseline is 1, the sum of proportions will always be >= 1  

Obviously, since the first two parameters will (most of the time) be the same for all assays, for the second and subsequent calculations, only the baseline dilution and sum of proportions have to be entered. 

On the VNT Calc tab, the Baseline dilution is the greatest dilution of serum that still neutralises all the virus in all the wells of that row, and the proportions are the proportions of wells that do not show infection.

### Changes/upgrades
Please let me know if something does not work, or you have an idea for an improvement. For the record, I am not going to implement something that analyses whole plates and works out sums of proportions, since I consider it is more work to feed that information into a computer than to do the sum in my head; open to other ideas, though.

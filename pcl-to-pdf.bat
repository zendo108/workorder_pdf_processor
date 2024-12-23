REM The follwowing script converts all pcl files to image base pdfs
@echo off
for %%I in (*.pcl) do gpcl6win64.exe -dNOPAUSE -sDEVICE=pdfwrite -sOutputFile="%%~nI.pdf" "%%I"

:: Improved suggested script that tries to generate a searchable text pdf format rather than image text
@echo off
for %%I in (*.pcl) do (
    gpcl6win64.exe -dNOPAUSE -sDEVICE=pdfwrite ^
    -sOutputFile="%%~nI.pdf" ^
    -dEmbedAllFonts=true ^
    -dSubsetFonts=true ^
    -dUseCIEColor ^
    -dCompressFonts=true ^
    -dAutoRotatePages=/PageByPage ^
    "%%I"
)

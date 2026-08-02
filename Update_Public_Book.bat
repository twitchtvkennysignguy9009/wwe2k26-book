@echo off
REM ============================================================
REM  Refresh the PUBLIC read-only book with the latest Playbook
REM  data (roster / factions / tournaments / season), then push.
REM  The public page rebuilds within ~1 minute.
REM ============================================================
setlocal
set "PUB=%~dp0"
set "BOOK=F:\talkshow-podcast\wwe2k26\main_book"
set "APP=F:\talkshow-podcast\wwe2k26\main_book\app"

echo Copying the latest book data...
copy /Y "%APP%\name-reviewer\reviewer_state.json"        "%PUB%data\reviewer_state.json"   >nul
copy /Y "%APP%\tournament-app\tournament_data.json"      "%PUB%data\tournament_data.json" >nul
copy /Y "%APP%\season-tracker\season_data.json"          "%PUB%data\season_data.json"     >nul
copy /Y "%BOOK%\default_roster.json"                     "%PUB%data\default_roster.json"  >nul
copy /Y "%APP%\wwe2k26tagteambuilder\teams_state.json"   "%PUB%data\teams_state.json"     >nul
copy /Y "%APP%\femalepicker\roster_state.json"           "%PUB%data\roster_state.json"    >nul
copy /Y "%APP%\sorter\sorter_data.json"                  "%PUB%data\sorter_data.json"     >nul
copy /Y "%APP%\sorter\sorter_locks.json"                 "%PUB%data\sorter_locks.json"    >nul
copy /Y "%BOOK%\match_types.json"                        "%PUB%data\match_types.json"     >nul

cd /d "%PUB%"
git add -A
git -c user.email="kenny199009@gmail.com" -c user.name="twitchtvkennysignguy9009" commit -m "Update book %date% %time%"
if errorlevel 1 (
  echo.
  echo Nothing new to publish - the book is already up to date.
) else (
  git push
  echo.
  echo Published. The public book refreshes in about a minute:
  echo   https://twitchtvkennysignguy9009.github.io/wwe2k26-book/
)
echo.
pause

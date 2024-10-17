{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "1. Basic Metonic Cycle Equation\n",
    "\n",
    "The Metonic cycle is based on the observation that 19 solar years are almost exactly equal to 235 lunar months.\n",
    "\n",
    "$19 Y_s \\approx 235 M_l$\n",
    "\n",
    "Where:\n",
    "\n",
    "$Y_s$ is the length of a solar year\n",
    "$M_l$ is the length of a lunar month\n",
    "\n",
    "Numerically:\n",
    "\n",
    "19 * 365.2425 days ≈ 235 * 29.53059 days\\\n",
    "6939.6075 days ≈ 6939.6885 days\\\n",
    "The difference is approximately 0.081 days over 19 years."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "2. Calendar Drift Calculation\n",
    "\n",
    "To calculate the drift between the Islamic and Gregorian calendars:\\\n",
    "$D = N * (235M_l - 19Y_s) + R * (Y_s - Y_i)$\n",
    "\n",
    "Where:\n",
    "\n",
    "$D$ is the total drift in days\\\n",
    "$N$ is the number of complete Metonic cycles\\\n",
    "$M_l$ is the length of a lunar month (29.53059 days)\\\n",
    "$Y_s$ is the length of a solar year (365.2425 days)\\\n",
    "$Y_i$ is the length of an Islamic year (354.36707 days)\\\n",
    "$R$ is the number of remaining years after complete Metonic cycles"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "3. Calculating Complete Metonic Cycles\n",
    "\n",
    "$N = \\lfloor \\frac{Y_f - Y_k}{19} \\rfloor$\n",
    "\n",
    "Where:\n",
    "\n",
    "$N$ is the number of complete Metonic cycles\\\n",
    "$Y_f$ is the future Gregorian year\\\n",
    "$Y_k$ is the known Gregorian year\\\n",
    "$\\lfloor \\rfloor$ denotes the floor function"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "4. Remaining Years Calculation\n",
    "\n",
    "$R = (Y_f - Y_k) \\bmod 19$\n",
    "\n",
    "Where:\n",
    "\n",
    "$R$ is the number of remaining years\\\n",
    "$\\bmod$ is the modulo operation"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "5. Converting Drift to Islamic Calendar Units\n",
    "\n",
    "Islamic Years Passed:\n",
    "\n",
    "$Y_p = \\lfloor \\frac{D}{Y_i} \\rfloor$\n",
    "\n",
    "Where:\n",
    "\n",
    "$Y_p$ is the number of Islamic years passed\\\n",
    "$D$ is the total drift in days\\\n",
    "$Y_i$ is the length of an Islamic year\n",
    "\n",
    "Remaining Days:\n",
    "\n",
    "$D_r = D \\bmod Y_i$\n",
    "\n",
    "Where:\n",
    "\n",
    "$D_r$ is the remaining days after counting complete Islamic years\n",
    "\n",
    "Islamic Months Passed:\n",
    "\n",
    "$M_p = \\lfloor \\frac{D_r}{29.53059} \\rfloor$\n",
    "\n",
    "Where:\n",
    "\n",
    "$M_p$ is the number of Islamic months passed in the final year"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "6. Predicting Future Islamic Date\n",
    "\n",
    "Year:\n",
    "\n",
    "$Y_f^i = Y_k^i + Y_p$\n",
    "\n",
    "Where:\n",
    "\n",
    "$Y_f^i$ is the future Islamic year\\\n",
    "$Y_k^i$ is the known Islamic year\n",
    "\n",
    "Month:\n",
    "\n",
    "$M_f^i = ((M_k^i + M_p - 1) \\bmod 12) + 1$\n",
    "\n",
    "Where:\n",
    "\n",
    "$M_f^i$ is the future Islamic month\\\n",
    "$M_k^i$ is the known Islamic month\n",
    "\n",
    "Day:\n",
    "\n",
    "The day calculation is approximate and often kept the same as the known day for simplicity. For more accuracy, complex algorithms considering the variable length of Islamic months are required."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "7. Accuracy Considerations\n",
    "\n",
    "- The Metonic cycle itself has a small error (about 2 hours over 19 years).\n",
    "- Islamic calendar months officially begin with the sighting of the new moon, which can vary from calculated dates.\n",
    "- Long-term predictions accumulate errors and should be used as approximations."
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

"""
entity_cards_data
-----------------

Entity cards data definitions.

:Author: Dario Garigliotti
"""

# -----------------
# -----------------
#  Constants
# -----------------

POSSIBLE_DATE_PROPS = ["birthDate", "birthdate", "dateOfBirth", "birthhdate", "dateBirth", "datebirth", "dateofbirth",
                       "releaseDate", "releasedate", "beginDate", "dateissue", "foundationdate", "foudationDate",
                       "pubDate", "productiondate", "foundationDate", "dateOfBith", "airingDates", "deadDate",
                       "dateOfBirthDecember", "nationalUpdate", "msrpDate",
                       "ruNationalteamupdate", "finalDate", "inventDate", "dateListed", "updatet", "castrationDate",
                       "designatedDate", "dateStart", "dateDeNaissance", "assetsDate", "lastfcdate", "dateOfIssue",
                       "oringalairdate", "firstengairdate", "lAtestReleaseDate", "reissueDate", "previewDate",
                       "dateDiscovered", "nextMatchupDate", "startingDate", "foundDate", "startDates",
                       "refLegalMandate", "lastipldate", "onidate", "placeOfDeathDate", "dateOfRebirth", "defenseDate",
                       "firstUkAirdate", "pcUpdate", "ruClubupdates", "eraDates", "datePost", "nupdate", "targetDate",
                       "fightDate", "beatifiedDate", "villageDate", "dateDrafted", "dateCompleted",
                       "constructionFinishDate", "dateRatified", "rearguedate", "dateCons", "productionDate",
                       "equityDate", "rlNtupdate", "dateSealed", "opendate", "extinctionDate", "origdates",
                       "airDate", "leaderTodate", "dateRepeal", "ptupdate", "surrenderDate", "designationDate",
                       "nationUpdate", "adminStructureDate", "ruUpdate", "interiorDate", "diedDate", "dateOfPremiere",
                       "articleDate", "debutdate", "convictionDate", "altdate", "datedecided", "rebuildDate",
                       "referralDate", "engineDate", "latestBetaDate", "latestReleaseDate", "fifaMinDate", "dateform",
                       "withdrawndate", "prodDate", "nextDate", "catDate", "lastAiringDate", "asianDateF", "cupdate",
                       "deathDateDeathPlace", "billDate", "udated", "finaldate",
                       "lastAirdate", "licenceDate", "ntUpdated", "foundedDate", "dateEnacted", "dateExtra",
                       "christenedDate", "dateOpening", "dateConfCommittee", "demiseDate", "issueDate",
                       "partyOfCandidate", "airdatet", "vitalDates", "useEwDate", "latestReleaseUpdates", "onAirDate",
                       "witdrawndate", "asasasadate", "datePublished", "dateAct", "abolishmentdate", "baptizedDate",
                       "notifydate", "builddate", "certdate", "deathvdate", "englishairdate",
                       "repealDate", "acquisitionDate", "datesActive", "decayDate", "metroAreaPopDate",
                       "dateDeMiseÀJour", "ruAmUpdate", "keysDates", "prevMatchupDate", "herkunftDerSoldaten",
                       "publishDate", "versiondate", "dateRepealed", "establistedDate", "pubDateOfEyesLikeStars",
                       "dateShowBegan", "consecratedDate", "extinctDate", "undergradate", "lastfirstclassdate",
                       "fileddate", "panDate", "reconstructionDate", "maxDate", "dateArgued", "charterdate", "nyupdate",
                       "dateRange", "releasingDate", "southDateopened", "dissolvedDate", "homeaccessdate", "datepassed",
                       "closeddate", "magazineLaunchDate", "dateOpen", "treasuryDate", "vetoeddate", "dateDecided",
                       "censorDate", "effectiveDate", "datePremiered", "firstodidate", "dateOfIntroduction",
                       "dateOfHighestRanking", "ruReupdate", "originalAirdate", "sbDate", "datePre",
                       "thesisDate", "dateType", "dateExt", "metroAreaDate", "licensedreldate", "renovationDate",
                       "abdicationDate", "tupdate", "dateFlooded", "delistedDateExtra", "trackRecordDate", "cdaghDate",
                       "firstMeetingDate", "latestMaintenanceDate", "dateOfDeaath", "demoCensusDate",
                       "dateOfFirstRelease", "ethnicDate", "datewithdrawal", "dateFiled", "dateFirstUse", "keyDate",
                       "dateEnd", "rtmDate", "大原さやかdate", "musicDate", "yrDate", "publDate", "deploymentDate",
                       "headmasterDates", "majorLeagueDebutdate", "urbanPopDate", "dateOfDiaconalOrdination",
                       "dateDissolved", "statsenddate", "datePopTotale", "partialdates", "festivalDates",
                       "establishedDate", "consolidatedRevenue", "dateMaxArea", "nationalDate", "canonizedDate",
                       "dateExpiration", "ruPcupdate", "majorExtensionDate", "dateAdopted", "abolishedDate",
                       "constructionDate", "declarationDate", "cjDate", "dateOfSamadhiTaken", "lastrundate",
                       "decisionDate", "dateOfFuneral", "matchDate", "operationDate", "lastAirDate", "playoffsDates",
                       "caughtDate", "useSeDate", "heardDate", "ruAmupdate", "dateOfEquipping", "premierDate",
                       "popDate", "dateDraft", "prodDesignDate", "submitdate", "chartdate", "germanPubDate",
                       "dateOfSamaadhi", "postDate", "datesOfOperation", "dateWon", "dateestablished", "councilDate",
                       "planDate", "ceaseDate", "closeDate", "datePopulation", "agricultureDate", "dateOfBrith",
                       "ministerialMeetingDates", "birthDates", "fromDate", "nextDates", "commissionDate",
                       "originalClosingDate", "unsigneddate", "dateOfIncorporation", "update", "htUpdate",
                       "disestablishedDate", "nationalteamUpdate", "fallDate", "dateOfPublishing", "binomialDate",
                       "argueddate", "resignationDate", "dateClosed", "dateInaugrated", "incorporationDate",
                       "latestPreviewReleaseDate", "airdates", "mokshaDate", "pCupdate", "birthDateBirthDate",
                       "olympicDate", "chiefJusticeDate", "designDate", "toppedOutDate", "ruNatupdate", "altdates",
                       "dvdreleasedate", "departureDate", "popMetroDate", "circulationDate", "deathDate", "decideddate",
                       "dateOfComposition", "retiredate", "bullDate", "foreignersDate", "mandateEnd", "dateSentenced",
                       "rebuiltdate", "firstukairdate", "asianDateQ", "ncupdate", "transdate", "lgupdate", "useDates",
                       "closingDate", "ruProclubupdate", "dateOfDeathOfLastChief", "chyavanaDate", "fcdebutdate",
                       "clubUpdate", "demoElectorsDate", "removeDate", "urbanAreaDate", "addedDate",
                       "dateOfProduction", "dateRestored", "remodelationDate", "birthDateb", "supersededByDate",
                       "enplanementsDate", "finalAirDate", "finaltdate", "firstAirDate", "frequentlyUpdated",
                       "dateOfDogbirth", "pubdate", "withdrawndates", "dateEventPre", "premiereDate", "launchedDate",
                       "dateHeCommitted", "dateOf", "ordinationDate", "asianDate", "christeningDate", "delistedDate",
                       "birthDatel", "dateopened", "altPublishDate", "popLatestDate", "dateOfDeathChildren",
                       "ruProvinceupdate", "dateOfBit", "delsitedDate", "localNewsNowAirdate", "pcuupdate", "splitdate",
                       "datefrom", "dedicatedDate", "designerDate", "inaugurationDate", "dateDestroyed", "buildDate",
                       "obverseDesignDate", "ruAmateurupdate", "disapDate", "festivalDate", "ordainedDate",
                       "dateOfDethrone", "arguedateb", "frequentlyUpdates", "dateOfBorth", "dateStarted",
                       "repubPubDate", "gfDate", "foundingDate", "englishPubDateTranslation", "dateOfAward",
                       "releasDate", "builtDate", "presentedDate", "ruClubuopdate", "causeForCanonizationDate",
                       "groundbreakingDate", "destructionDate", "dateOfSuspension", "gamesDateF", "spanishReleaseDate",
                       "dateFounded", "accessioneudate", "activeDate", "reopeningDate", "dateFirstIssued",
                       "onlyodidate", "mandateStart", "haltedDate", "signeddate", "englishReleaseDate",
                       "constructionEndDate", "latinspanishairdate", "dateOfEath", "ruYouthdate", "updatePage",
                       "pbDate", "updateSummary", "latestTestReleaseDate", "datesClés", "presidentDate",
                       "dateregistereddomains", "lastdate", "rebuilddate", "outdated", "eloMinDate", "arrestDate",
                       "commitdate", "founderDate", "dateEatra", "retireddate", "dateminting", "venerableDate",
                       "initiationDate", "defunctDate", "formationDate", "publicationDate", "consolidatedLiabilities",
                       "dateOfConstruction", "dateOfIntroductionSource", "changeOfUseDate", "fianldate",
                       "ntupdateNegouse", "pfDate", "dateOfElevation", "nationalupdate", "attainmentDate", "polyDate",
                       "pcpdate", "completedDate", "nextMeetingDate", "releaseDates", "stateDate", "datend",
                       "dateOfBiologicalDeath", "dateWritten", "electionDate", "itfMaxDate", "dateApprehended",
                       "ipoDate", "dateOFDeath", "preReleaseDate", "officialLaunchDate", "previousDate",
                       "dateOfAbdication", "dateCommenced", "originalreldate", "currentCatDateRef",
                       "nationalteamupdate", "dateOfInduction", "listingDate", "dateSans", "rededicationDate",
                       "secededdate", "baptismDate", "quarterreleasedate", "europeairdate", "cupDate", "rebuildDates",
                       "contractenddate", "openingDate", "siMadeDate", "buildingDate", "dateOfEstablishment",
                       "placeDate", "dateLastUse", "fondateur", "onlydate", "withdrawaldate", "clubupdate",
                       "creationDate", "dvdReleaseDate", "firstclassdebutdate", "dateOfDisplay", "hbmdate", "dateDate",
                       "odilastdate", "dateOfPriestlyOrdination", "compositionDate", "compdate", "kshDate",
                       "replacementDate", "dateOfArrest", "finishDate", "dateEcent", "dateInaugrationOn", "laborDate",
                       "enrollmentDate", "rlAmupdate", "visitationDate", "todate", "inceptdate", "introduceddate",
                       "proposedDate", "preselectionDate", "sigdate", "movedDate", "firstPublicReleaseDate",
                       "dissolutionDate", "statsUpdate", "gamesDateQ", "mayorDate", "datecopied", "perciousDate",
                       "disappearedDate", "readmittancedate", "leaderDate", "ntUpdate", "dateEstablished", "imagedate",
                       "natupdate", "reverseDesignDate", "viewDate", "dateTo", "dateEventEnd", "serviceDates",
                       "deathdate", "igDate", "dateRest", "nationalTeamupdate", "combinedDate", "consecrationdate",
                       "firstDate", "offAirDate", "dateOfCremation", "repUpdate", "conferencedate", "dateAssented",
                       "navyDate", "eletionDate", "expansionDate", "terminationDate", "arrivalDate", "locationsDate",
                       "ruCoachupdate", "datesOfExistence", "commissioningDate", "orderMandate", "admittancedate",
                       "decommissionedDate", "licenseDate", "introductionDate", "launchdate", "updateMethod",
                       "frequencyUpdate", "lastgamedate", "regSeasonDates", "ruSevensupdate", "originalAirDate",
                       "dateResolution", "warDate", "landingDate", "degignDate", "accessdate", "versionBetaDate",
                       "grandOpeningDate", "dateConc", "dateOfExpiry", "isolationDate", "numberDate",
                       "discontinuedDate", "startDateEast", "closedDate", "accessionEuDate", "dissetablishedDate",
                       "dateFrom", "publicationDateEn", "populationdate", "isolationdate", "lastodidate",
                       "rearguedatea", "dateHeard", "arguedatea", "releasedDate", "updateCitations", "coorindatesScale",
                       "dateApp", "repupdate", "increaseDate", "decidedDate", "engReleaseDate", "passeddate",
                       "ntcupdate", "releaseDate(inBookForm)", "firstFlightDate", "versionDate", "championDate",
                       "sdDate", "usAirdate", "dateofdetah", "itfMinDate", "latinspanishlairdate", "backDate",
                       "dvdReleaseDates", "movieReleaseDate", "accessDate", "sooupdate", "deliverydate",
                       "dateImplementation", "benchmarkDate", "coordinatesDate", "airdatemusicFrequency", "hofdate",
                       "statdate", "dateOfCurrentRanking", "firstipldate", "betaTestDate", "nationateamUpdate",
                       "estabslishedDate", "dateAgreeded", "updates", "pbupdate", "updateDate", "returnDate",
                       "demolishedDate", "semiDate", "datesOfIssue", "sigdateLabel", "kevalgyanDate", "dateOfMerger",
                       "dvd&BluRayReleaseDate", "dateOfPublication", "lastReleaseDate", "dateGamePlayed", "scrapdate",
                       "firstrundate", "natinalteamUpdate", "pausedDate", "pyramidDate", "dateUse", "fiinaldate",
                       "dateOfOrigin", "filmingDate", "populationDate", "serviceEndDate", "lstdate",
                       "latestUpdate", "pubEnglishDate", "burialDate", "originDate", "reReleaseDate", "aj9Date",
                       "dateOfPlace", "relocatedDate", "consolidatedAssets", "agreeddate", "ruRefereeupdate",
                       "fdDate", "origdate", "allStarDate", "dateComp", "popUrbanDate", "dateOfBurial", "popdate",
                       "spDate", "consolidatedResult", "game9Date", "testdeubutdate", "dayOfLastUpdate",
                       "surrenderedDate", "openDate", "danceDate", "reOpeningDate", "conceptionDate",
                       "lasttestdate", "deorbitDate", "orbitalInsertionDate", "creationdate",
                       "projectImplementationDate", "dateOfConsecration", "lastplayeddate", "otherCandidates",
                       "iihfMaxDate", "altDeathDate", "dateCreation", "supersededDate",
                       "argueDate", "endDate", "vicePresidentDate", "homedate", "week9date", "dateDerogated", "bradate",
                       "dateOfBir", "duplicateDateStart", "productionDates", "dateOfChristening", "reldate",
                       "suspensionDate", "dateOfYear", "airdater", "datepop", "dateOfCompilation",
                       "dateDemolished", "awardDate", "settledDate", "onlytestdate", "ntupadate", "gamesDate",
                       "fromdate", "datePromulgated", "ifoundingDate", "startDate", "dateOfLaunch", "cdDate",
                       "thomasWilkinsonAirdate", "registrationDate", "mandateperiod", "debutDate", "dateOfRelease",
                       "constructionStartDate", "fecDate", "dateprefix", "dateOfFinalPerformance", "rankDate",
                       "templeDates", "dateSigned", "initialReleaseDate", "clubCupdate", "dateEvent", "rearguedateb",
                       "samadhiDate", "dateformat", "birhDate", "accessdates", "natonalteamUpdate", "birthDateHuih",
                       "lastUpdated", "tmupdate", "englishPublicationDate", "fulldate", "raNtupdate", "gaDate",
                       "discoveredDate", "dateretired", "constructionDates", "enddate", "finalUpdate", "datelol",
                       "decisiondate", "originalairdate", "founderDates", "dateCreatedCardinal", "dateref",
                       "ruCliubupdate", "dateDeath", "dateAfter", "shutdownDate", "suppressedDate", "lyricsDate",
                       "dateOfDisappearance", "actualDate", "laestdate", "altdatet", "dateYofBirth", "dateFin",
                       "depositionDate", "firstAirdate", "dateDensity", "dateRenovated", "sectionDate", "dateIfFail",
                       "dateOfDeathS", "dateFormat", "siLaidDate", "servicedates", "pcupdate", "gazetteDate",
                       "dateSubmitted", "copyrightDate", "subscriberDate", "alternativeDateOfDeath", "testdebutdate",
                       "toDate", "rlCoachupdate", "dateBuilt", "relDate", "constructedDate", "firstReleaseDate",
                       "nationaltemplateUpdate", "ruNtupdate", "dieDate", "dateDeveloped", "dateofDeath", "reupdate",
                       "birthDateAndAge", "demolitionDate", "ifacMembershipDate", "commerceDate", "dateFormed",
                       "dateouverture", "recDate", "asofdate", "previousReleaseDate", "alternativeDateOfBirth",
                       "renameDate", "firstdate", "firsttestdate", "usReleaseDate", "brithDate", "reEquipmentDate",
                       "dateEnteredIntoForce", "liquidated", "establishDate", "renovatedDate", "numEmployeesDate",
                       "originlairdate", "updated", "restingDate", "dateMade", "dateOfDeath", "siddhiDate",
                       "iihfMinDate", "officialListingDate", "odidebutdate", "overriddendate", "northDateopened",
                       "latestTestDate", "entrydate", "japaneseairdate", "odDate", "clupdate", "beginningDate",
                       "statusDate", "dateOfBirth&nbsp;&nbsp;", "latestPreviewDate", "updateProteinBox", "upadated",
                       "fifaMaxDate", "municipalStructureDate", "airdate", "dateOfMarriage", "bornDate", "ukairdate",
                       "dikshaDate", "dateto", "monthAndDate", "prevDates",
                       "club–update", "justiceDate", "openedDate", "urlDateArg", "firstCommissionedDate", "sectiondate",
                       "marriageDate", "retireDate", "dateOfOpening", "discoveryDate", "celebrationDate",
                       "birthDateName", "scheduledReleaseDate", "dateActive", "currentCatDate", "uProvinceupdate",
                       "dateEventt", "useUsDate", "datePop", "softOpeningDate", "charteredDate", "recoveryDate",
                       "dateDissipated", "icupdate", "datePassed", "superDate", "pDates", "natioanlteamUpdate",
                       "subjectDates", "flybyDate", "clubteamUpdate", "betaLaunchDate", "betaReleaseDate",
                       "updateModel", "lastMeetingDate", "dateFormats", "manpowerDate", "nttupdate", "updatemodel",
                       "dateofdeath", "elecDate", "originalairDate", "constructionStarDate", "nextExpectedReleaseDate",
                       "frstdate", "worldDateF", "affdate", "releaseDate(s)", "nationalTeamUpdate", "rlClubupdate",
                       "datesExcavated", "dedicationDate", "discontinuationDate", "dateConst", "fsDate",
                       "indianAirDate", "ntupdate", "canonisedDate", "veneratedDate", "websiteLaunchDate",
                       "bluRayReleaseDate", "relaunchDate", "dateCreated", "multiplereleasedates", "dateOfDeaths",
                       "firstTrophyMeetingDate", "currentStartDate", "shdates", "effectivedate", "establishedDates",
                       "redesignDate", "ganderDayDate", "announcedDate", "dateMarch", "inprocessDate", "datesRecorded",
                       "restoredate", "ruCupdate", "ruNationalupdate", "accessdatew", "consecrationDate", "dateOpened",
                       "monthDate", "closedate", "dateEffective", "dateOfRet", "cgDate", "firstUseDate", "ntpdate",
                       "servDesignDate", "decidedate", "governorDate", "establishmentDate", "worldDateQ",
                       "petitiondate", "bowlDate", "showUpdates", "endglishPubDate", "dateExpiry", "cityrightsDate",
                       "birthDateY", "apprehensionDate", "revivalDate", "runDate", "rehabilitationDate",
                       "settlementDate", "ruClubupdate", "incorporatedDate", "archivedate", "titleDate",
                       "officialUpdateAccounts", "eloRatingMaxDate", "consoildated", "closureDate", "dateDens",
                       "marrieddate", "namechangedate", "arguedate", "censusDate", "introdate",
                       "maccabiahDate", "championshipDate", "dateAired", "statisticsDate", "ncDate", "worldDate",
                       "nationalteamTupdate", "birthDateAge", "testDebutDate", "playoffsDate", "mandate",
                       "inflationSourceDate", "launchDate", "englishPubDate", "npiasDate", "startdate", "dateprinting",
                       "dateOfBith", "completionDate", "eloMaxDate", "quarterDate", "maxCountDate", "fwDate",
                       "ntudpdate", "expectedCompletionDate", "spillDate", "lastupdate", "lastDate",
                       "birthYear", "deathYear", "formation", "formationYear"]

POSSIBLE_PLACE_PROPS = ["birthPlace", "PlaceOfBirth", "bbirthPlace", "beatifiedPlace",
                        "biRthPlace", "biejjjrthPlace", "birghPlace", "birhPlace", "birtPlace", "birth)place",
                        "birthBirthplace", "birthPlacE", "birthPlaceDeathSeptember", "birthdplace",
                        "birthplace", "birth°place", "biryhPlace", "bitheplace", "accidentPlace",
                        "alternativePlaceOfDeath", "arrestPlace", "asianPlace",
                        "asianPlaceF", "asianPlaceQ", "backPlace", "baptismPlace", "bornPlace",
                        "brithPlace", "bodyDiscoveredPlace", "burailPlace", "burial+place", "burialPlace",
                        "buriedPlace", "burilaPlace",
                        "canonisedPlace", "canonizedPlace", "castrationPlace", "causeForCanonizationPlace",
                        "championshipPlace", "christeningPlace", "chyavanaPlace", "cityofbirthPlace", "confPlace",
                        "conferencePlace", "cremationPlace", "currentBirthPlace", "currentPlace", "currentlyPlace",
                        "dateOfPlace", "deahPlace", "deahplace", "deatgPlace", "death+place", "deathDateDeathPlace",
                        "deathPlace", "deathplace", "decisionplace", "declaredVenerablePlace", "desthPlace",
                        "diedPlace", "dikshaPlace", "dirthplace", "disappearedPlace", "discoveredPlace", "displaced",
                        "displacement", "divisionPlace", "divisionalPlace", "establishedPlace", "euroReplaceCash",
                        "euroReplaceNonCash", "facebookPlaces", "fondedPlace", "formerWorkplaces", "foundationPlace",
                        "foundedPlace", "fourthPlace", "fourthplace", "futureRestingPlace", "gamesPlace", "gamesPlaceF",
                        "gamesPlaceQ", "hailsPlace", "hbmplace", "homePlace", "igPlace", "imagePlace", "importantPlace",
                        "initiationPlace", "interrmentPlace", "jeevaSamadhiPlace", "jeevasamadhiplace",
                        "kevalgyanPlace", "kidnappingPlace", "leaguePlace", "licensePlace", "livePlace", "livingPlace",
                        "livingPlaces", "locationPlace", "maccabiahPlace", "mainPlace", "mainplace", "marriagePlace",
                        "meetingPlace", "mokshaPlace", "mukthiPlace", "nameReplacedBy", "nationalPlace", "nativePlace",
                        "nbirthPlace", "ncaafourthplace", "olympicPlace", "oplaceOfBirth", "originPlace", "originplace",
                        "otherPlaces", "pCode(placeCode)", "panPlace", "parkingPlaces", "pistonDisplacement",
                        "placeActually", "placeBirth", "placeDate", "placeDeath", "placeDiscovered", "placeName",
                        "placeOfArrest", "placeOfBerth", "placeOfBiirth", "placeOfBir", "placeOfBirh", "placeOfBirth",
                        "placeOfBirth&nbsp;&nbsp;", "placeOfBirthPlace", "placeOfBirtht", "placeOfBirth—",
                        "placeOfBith", "placeOfBrith", "placeOfBurial", "placeOfBurialLabel", "placeOfChristening",
                        "placeOfCitizenship", "placeOfCollege", "placeOfConsecration", "placeOfCremated",
                        "placeOfCremation", "placeOfDeadth", "placeOfDeah", "placeOfDeat", "placeOfDeatH",
                        "placeOfDeath", "placeOfDeathDate", "placeOfDeathJoinedClub", "placeOfDeathKids",
                        "placeOfDeathPlace", "placeOfDeathplace", "placeOfDeathv", "placeOfDeeath",
                        "placeOfDiaconalOrdination", "placeOfDirection", "placeOfEntombment", "placeOfFuneral",
                        "placeOfLastRites", "placeOfLivingAndWork", "placeOfMarriage", "placeOfOrigin",
                        "placeOfPriestlyOrdination", "placeOfPublication", "placeOfRelease", "placeOfResidence",
                        "placeOfRest", "placeOfResting", "placeOfSamadhi", "placeOfSchooling", "placeOfStudy",
                        "placeOfWork", "placeOrigin", "placeRested", "placeSemi", "placeSigned", "placeType",
                        "placebirth", "placeburial", "placecat", "placedby", "placeifburialLabel", "placement",
                        "placementCellWebsite", "placementOfficer", "placements", "placename", "placeofbirth",
                        "placeofburial", "placeofburial+label", "placeofburialCoordinates", "placeofburialLabel",
                        "placeofburialLanel", "placeofburiedness", "placeofdeath", "placeofresidencel", "placeofrest",
                        "placeofurialLabel", "placesOfInterest", "placesSituatedFamous", "placesofinterest", "poplace",
                        "popplace", "publicationPlace", "releasePlace", "replace", "replaceNames", "replaceability",
                        "replaced", "replaced+by", "replacedBy", "replacedByNames", "replacedChannel", "replacedNames",
                        "replacedWith", "replacedby", "replacedwho", "replacedyear", "replacement", "replacementDate",
                        "replaces", "residencePlace", "resingPlace", "resingplace", "restPlace", "restiingPlace",
                        "resting+place", "restingPlace", "restingPlaceCoordinates", "restingPlaceLabel",
                        "restingPlaced", "restingplace", "restingplacecoordinates", "restingplacelatd", "restomgPlace",
                        "restrictedPlacesSections", "restrictedPlacesSynopsis", "rustingPlace", "samadhiPlace",
                        "secondPlace", "shipDisplacement", "shipDisplacement(empty)", "shipDisplacement(full)",
                        "shipFullDisplacement", "shipGrossDisplacement", "shipPlaceOfConstruction",
                        "shipPlacedOutOfService", "shotingPlace", "siddhiPlace", "startPlace", "thirdPlace",
                        "thirdplace", "titleplace", "trackPlace", "ttBestPlace", "typeOfPlace", "veneratedPlace",
                        "villagePlace", "visitorPlace", "willedPlace", "wokplace", "workPlace", "workPlaces",
                        "workplace", "workplaces", "worldPlace", "worldPlaceF", "worldPlaceQ"
                        ]

POSSIBLE_LOCATION_PROPS = ["location", "headquarter", "headquarters",
                           "additionalLocation", "additionalLocations", "addnlLocation", "allLocations", "allocation",
                           "alocationCity", "alternativeLocationMap", "arenaLocation", "ashtangaLocations",
                           "birthLocation", "broadcastLocation", "burialLocation", "capitalLocation",
                           "championshipLocation", "clubhouseLocation", "confluenceLocation", "corporateLocation",
                           "creationlocation", "crossesLocation", "currentLocation", "currentraininglocations",
                           "currenttraininglocations", "deathLocation", "dischargeImperialLocation",
                           "dischargeLocation", "discoveryLocation", "displayLocation", "divisionLocation",
                           "earlyLocation", "ecrilocation", "elevationLocation", "engineLocation", "epicenterLocation",
                           "facilityLocations", "factoryLocation", "filmLocation", "filmLocation(s)", "filmOfLocation",
                           "filmingLocation", "filmingLocations", "finalLocation", "firmLocation", "firstLocation",
                           "flLocation", "formerLocation", "formerLocations", "formerlocations",
                           "formertraininglocations", "formerttraininglocations", "foundationLocation",
                           "foundedLocations", "foundingLocation", "geolocation", "gfLocation", "googleLocation",
                           "governmentLocation", "headOfficeLocation", "headquartersLocation", "headquartersLocations",
                           "highestLocation", "highestLocationNote", "homeLocation", "hqLocation", "hqLocationCity",
                           "hqLocationCountry", "imageLocation", "iwiLocation", "ladieslocations", "landMarkOfLocation",
                           "launchLocation", "legacylocation", "location(marketing)", "location(s)",
                           "location(steelDivision)", "location(temporary)", "locationAddress", "locationAlt",
                           "locationArea", "locationAudio", "locationCities", "locationCity", "locationColor",
                           "locationContry", "locationCountries", "locationCountry", "locationCounty", "locationCoutry",
                           "locationDescription", "locationDir", "locationDirector", "locationDist", "locationDistMi",
                           "locationDrafted", "locationEu", "locationFactory", "locationFilming", "locationFor",
                           "locationHeader", "locationHeadquarters", "locationIn", "locationInAfghanistan",
                           "locationInPakistan", "locationManager", "locationMap", "locationMapAlt",
                           "locationMapCaption", "locationMapLabelPosition", "locationMapRelief", "locationMapSize",
                           "locationMapText", "locationMapWidth", "locationName", "locationNote", "locationOfDeath",
                           "locationOfDocument", "locationOfHeadquarters", "locationOfHighestMount", "locationOfMill",
                           "locationOfProduction", "locationOn", "locationPerformed", "locationPlace",
                           "locationPresence", "locationProvince", "locationPublic", "locationRegion", "locationScout",
                           "locationServices", "locationSetting", "locationSigned", "locationSound",
                           "locationSoundRecording", "locationSpecial", "locationState", "locationStreet",
                           "locationTechnologies", "locationTitle", "locationTown", "locationTs", "locationType",
                           "locationUs", "locationalStatus", "locationarticle", "locationcity", "locationmap",
                           "locationsCity", "locationsCountry", "locationsDate", "locationsOfColleges",
                           "locationsOfPeace", "lowestLocation", "lowestLocationNote", "mainLocation",
                           "managementLocation", "managementLocationType", "mapLocation", "maxLocation",
                           "memberLocations", "menlocations", "mouthLocation", "municipalLocation", "ncLocation",
                           "noLocationProperty", "noOfLocations", "numLocationYear", "numLocations", "numLocationsYear",
                           "numberLocations", "numberOfLocations", "officeLocation", "officeLocations",
                           "originalLocation", "othLocation", "otherFormerLocations", "otherLocation", "otherLocations",
                           "payloadLocation", "pfLocation", "practiceLocation", "premiereLocation", "presentLocation",
                           "previousLocation", "previousLocations", "pubLocation", "pushpinLocation",
                           "pushpinMapLocation", "recLocation", "recordLocation", "regionLocation", "releaseLocation",
                           "remLocation", "riverLocation", "saddleLocation", "salesLocation", "schoollocations",
                           "shipLocation", "shipwreckLocation", "shootingLocations", "shopLocation",
                           "sourceConfluenceLocation", "sourceLocation", "sourceLocationNote", "storeLocations",
                           "streetLocation", "studioLocation", "symbolLocation", "systemLocation", "tollPlazaLocations",
                           "traininglocations", "transmitterLocation", "wikimapLocation"
                           ]

POSSIBLE_OTHER_INTERESTING_PROPS = [
    # author or person in charge
    "author", "creator", "ceo", "founder", "chairman", "almaMater",
    "almaMáter", "almamater", "president", "mayor", "leaderName", "manager",
    # places
    "populationTotal", "country", "region", "area", "postalCode", "subdivisions",
    "cityMotto", "coatOfArmsLegend", "party", "population",
    "areaMetro", "areaTotal", "areaUrban",
    "populationMetro", "populationUrban", "capacity",
    "nationality", "residence", "citizenship", "ethnicity", "league",
    # family
    "spouse", "children", "doctoralAdvisor",
    # works of art: movies, music, books
    "director", "Work/runtime", "cinematography",
    "artist", "genre", "recordLabel", "producer",
    "previousWork", "subsequentWork", "nextAlbum",
    "literaryGenre", "publisher", "language", "titleOrig",
    "writer", "distributor",
    # artistical/political field, movement
    "field", "movement",
    # events: conflicts, concerts
    "result", "partof", "conflict", "causalties", "combatant", "territory",
    "musicFestivalName"
    # "quote"  # not, since likely a long statement
]

# http://fontawesome.io/icons/
FAVICON_INFO = "fa fa-info-circle"
FAVICON_CAL = "fa fa-calendar"
FAVICON_MAP_MARKER = "fa fa-map-marker"
FAVICON_GLOBE = "fa fa-globe"  # it should never be used as it's reserved for entity Wikipedia/DBpedia/Home pages
FAVICON_BUILDING = "fa fa-building"
FAVICON_SUITCASE = "fa fa-suitcase"
FAVICON_HEART = "fa fa-heart"
FAVICON_GRAD_CAP = "fa fa-graduation-cap"
FAVICON_HOME = "fa fa-home"
FAVICON_INDUSTRY = "fa fa-industry"
FAVICON_MUSIC = "fa fa-music"
FAVICON_UNIVERSITY = "fa fa-university"
FAVICON_PAINTBRUSH = "fa fa-paint-brush"
FAVICON_PENCIL = "fa fa-pencil"
FAVICON_LIGHTBULB = "fa fa-lightbulb-o"
FAVICON_MICROPHONE = "fa fa-microphone"
FAVICON_FILM = "fa fa-film"
FAVICON_BOOK = "fa fa-book"
FAVICON_WRENCH = "fa fa-wrench"
FAVICON_QUOTE_LEFT = "fa fa-quote-left"
FAVICON_TIME = "fa fa-clock-o"  # "fa fa-hourglass", "fa fa-hourglass-half" and similars didn't work
FAVICON_LANGUAGE = "fa fa-language"
FAVICON_HISTORY = "fa fa-history"
FAVICON_USERS = "fa fa-users"
# Also
FAVICON_TROPHY = "fa fa-trophy"
FAVICON_CAR = "fa fa-car"
FAVICON_BELL = "fa fa-bell-o"
FAVICON_BUG = "fa fa-bug"
FAVICON_BUS = "fa fa-bus"
FAVICON_CAMERA = "fa fa-camera"
FAVICON_EYE = "fa fa-eye"
FAVICON_PHONE = "fa fa-phone"
FAVICON_PUZZLE = "fa fa-puzzle-piece"
FAVICON_PLANE = "fa fa-plane"
FAVICON_STAR = "fa fa-star"
FAVICON_TAGS = "fa fa-tags"
FAVICON_VOLUME = "fa fa-volume-up"
FAVICON_USER = "fa fa-user"
FAVICON_TREE = "fa fa-tree"
FAVICON_HEALTH = "fa fa-plus-square"
FAVICON_ID_CARD = "fa fa-id-card"
FAVICON_COGS_WHEELS = "fa fa-cogs"
FAVICON_FUTBOL = "fa fa-futbol-o"
FAVICON_BOLT = "fa fa-bolt"
FAVICON_COMMENT = "fa fa-comment"
FAVICON_COMMENTS = "fa fa-comments"
FAVICON_BIRTHDAY_CAKE = "fa fa-birthday-cake"

PROPS_ICONS = {  # Redefining keys collection, but in this way they keep priorities
    # author or person in charge
    "author": FAVICON_LIGHTBULB,
    "creator": FAVICON_LIGHTBULB,
    "ceo": FAVICON_SUITCASE,
    "founder": FAVICON_LIGHTBULB,
    "chairman": FAVICON_SUITCASE,
    "almaMater": FAVICON_LIGHTBULB,
    "almaMáter": FAVICON_LIGHTBULB,
    "almamater": FAVICON_LIGHTBULB,
    "president": FAVICON_SUITCASE,
    "mayor": FAVICON_BUILDING,
    "leaderName": FAVICON_USERS,
    "manager": FAVICON_USERS,
    # places
    "populationTotal": FAVICON_INFO,
    "country": FAVICON_INFO,
    "region": FAVICON_INFO,
    "area": FAVICON_INFO,
    "postalCode": FAVICON_BUILDING,
    "subdivisions": FAVICON_INFO,
    "cityMotto": FAVICON_QUOTE_LEFT,
    "coatOfArmsLegend": FAVICON_QUOTE_LEFT,
    "party": FAVICON_UNIVERSITY,
    "population": FAVICON_INFO,
    "areaMetro": FAVICON_INFO,
    "areaTotal": FAVICON_INFO,
    "areaUrban": FAVICON_INFO,
    "populationMetro": FAVICON_HOME,
    "populationUrban": FAVICON_HOME,
    "capacity": FAVICON_INFO,
    "nationality": FAVICON_HOME,
    "residence": FAVICON_HOME,
    "citizenship": FAVICON_INFO,
    "ethnicity": FAVICON_INFO,
    "league": FAVICON_INFO,
    # family
    "spouse": FAVICON_HEART,
    "children": FAVICON_HEART,
    "doctoralAdvisor": FAVICON_GRAD_CAP,
    # works of art: movies, music, books
    "director": FAVICON_FILM,
    "Work/runtime": FAVICON_TIME,
    "cinematography": FAVICON_FILM,
    "artist": FAVICON_PAINTBRUSH,
    "genre": FAVICON_MUSIC,
    "recordLabel": FAVICON_MUSIC,
    "producer": FAVICON_WRENCH,
    "previousWork": FAVICON_WRENCH,
    "subsequentWork": FAVICON_WRENCH,
    "nextAlbum": FAVICON_MUSIC,
    "literaryGenre": FAVICON_BOOK,
    "publisher": FAVICON_BOOK,
    "language": FAVICON_LANGUAGE,
    "titleOrig": FAVICON_LANGUAGE,
    "writer": FAVICON_PENCIL,
    "distributor": FAVICON_MICROPHONE,
    # artistical/political field, movement
    "field": FAVICON_INFO,
    "movement": FAVICON_PAINTBRUSH,
    # events: conflicts, concerts
    "result": FAVICON_INFO,
    "partof": FAVICON_INFO,
    "conflict": FAVICON_HISTORY,
    "causalties": FAVICON_HISTORY,
    "combatant": FAVICON_HISTORY,
    "territory": FAVICON_INFO,
    "musicFestivalName": FAVICON_MUSIC
    # "quote"  # not, since likely a long statement

}

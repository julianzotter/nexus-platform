# RFEM 5 COM – API-Referenz (automatisch aus der Typbibliothek erzeugt)

Quelle: `C:\Program Files\Common Files\Dlubal\RFEM5_64.dll` → comtypes-Modul `_5A027F61_50D6_4979_B4FB_A80F4B9FD2C3_0_5_7.py` (SHA-256 66a6ec64d0809aa5…) · 114 Interfaces · 184 Strukturen · 116 Aufzählungen

Lesart: `Methode(ein: Typ, …) → aus: Typ` – in Python liefert comtypes die `out`-Parameter als Rückgabewert (mehrere als Tupel). `X[]` = Array (SAFEARRAY) → Python-Liste/Tupel. Einheiten SI (N, Nm, m).

## Inhalt

1. Interfaces
2. Strukturen
3. Aufzählungen

## 1. Interfaces

### IAngularDimension

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Dimension: AngularDimension | Gets angular dimension parameters. |
| `SetData` | Dimension: AngularDimension* | – | Sets angular dimension parameters. |
| `Delete` | – | – | Deletes angular dimension. |

### IApplication

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `LockLicense` | – | – | Locks license. |
| `UnlockLicense` | – | – | Unlocks license. |
| `IsComLicensed` | – | Licensed: VARIANT_BOOL | Checks if COM is licensed. |
| `IsAppLicensed` | – | Licensed: VARIANT_BOOL | Checks if application is licensed. |
| `CreateModel` | Name: BSTR | Model: IModel | Creates model. |
| `OpenModel` | Path: BSTR | Model: IModel | Opens model. |
| `GetModelCount` | – | Count: c_int | Counts opened models. |
| `GetModel` | Index: c_int | Model: IModel | Gets model at index. |
| `GetActiveModel` | – | Model: IModel | Gets interface to the active model. |
| `Show` | – | – | Shows the hidden application. |
| `Close` | – | – | Closes the application. |
| `RefreshGUI` | – | – | Refreshes application GUI. |
| `GetVersion` | – | Version: BSTR | Gets version of the application. |
| `GetPath` | – | Path: BSTR | Gets path to the application's folder. |
| `GetLanguage` | – | Language: BSTR | Gets text identifier of the language currently used in the application. |
| `SetLanguage` | Language: BSTR | – | Sets language to be used in the application. |
| `SetStatusBarText` | Text: BSTR | – | Sets a text on the status bar. |

### IArcLengthDimension

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Dimension: ArcLengthDimension | Gets arc length dimension parameters. |
| `SetData` | Dimension: ArcLengthDimension* | – | Sets arc length dimension parameters. |
| `Delete` | – | – | Deletes arc length dimension. |

### IAverageRegion

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Region: AverageRegion | Gets average region parameters. |
| `SetData` | Region: AverageRegion* | – | Sets average region parameters. |
| `Delete` | – | – | Deletes average region. |

### IAverageRegions

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `PrepareModification` | – | – | Prepares application for data modification. |
| `FinishModification` | – | – | Finishes data modification and updates the model. |
| `CancelModification` | – | – | Cancels current data modification. |
| `Clean` | – | – | Cleans average regions objects. |
| `DeleteObjects` | List: BSTR | – | Deletes specified objects. |
| `SetObjectID` | No: c_int, At: ItemAt, ID: BSTR | – | Sets ID of the object. |
| `GetAverageRegionCount` | – | Count: c_int | Gets count of average regions. |
| `GetAverageRegion` | No: c_int, At: ItemAt | Region: IAverageRegion | Gets interface for working with average region. |
| `SetAverageRegion` | Region: AverageRegion* | IRegion: IAverageRegion | Sets average region and returns it's interface. |
| `GetAverageRegions` | – | Regions: AverageRegion[] | Gets array of average regions. |
| `SetAverageRegions` | Regions: AverageRegion[]* | – | Sets array of average regions. |

### IBSplineSurface

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetExtraData` | – | Surface: BSplineSurface | Gets B-Spline surface parameters. |
| `SetExtraData` | Surface: BSplineSurface* | – | Sets B-Spline surface parameters. |

### ICalculation

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetSettings` | – | Settings: CalculationSettings | Gets calculation settings. |
| `SetSettings` | Settings: CalculationSettings* | – | Sets calculation settings. |
| `GetOptions` | – | Options: CalculationOptions | Gets calculation options. |
| `SetOptions` | Options: CalculationOptions* | – | Sets calculation options. |
| `GetPrecisionAndTolerance` | – | Parameters: PrecisionAndTolerance | Gets precision and tolerance. |
| `SetPrecisionAndTolerance` | Parameters: PrecisionAndTolerance* | – | Sets precision and tolerance. |
| `GetNonlinearities` | – | Parameters: CalculationNonlinearities | Gets calculation nonlinearity parameters. |
| `SetNonlinearities` | Parameters: CalculationNonlinearities* | – | Sets calculation nonlinearity parameters. |
| `GetReactivation` | – | Parameters: ReactivationOfFailingMembers | Gets reactivation of failing members. |
| `SetReactivation` | Parameters: ReactivationOfFailingMembers* | – | Sets reactivation of failing members. |
| `GetInternalPressure` | – | Parameters: InternalPressure | Gets internal pressure parameters. |
| `SetInternalPressure` | Parameters: InternalPressure* | – | Sets internal pressure parameters. |
| `GetSolverMethod` | – | Method: SolverMethodType | Gets method for system of equations. |
| `SetSolverMethod` | Method: SolverMethodType | – | Sets method for system of equations. |
| `GetBendingTheory` | – | Theory: BendingTheoryType | Gets plane bending theory. |
| `SetBendingTheory` | Theory: BendingTheoryType | – | Sets solver version. |
| `GetSolverVersion` | – | Solver: SolverVersionType | Gets solver version. |
| `SetSolverVersion` | Solver: SolverVersionType | – | Sets solver version. |
| `GenerateFeMesh` | – | – | Generates FE mesh. |
| `DeleteFeMesh` | – | – | Deletes FE mesh. |
| `GetFeMesh` | – | Mesh: IFeMesh | Gets interface for working with FE mesh. |
| `GetFeMeshSettings` | – | Settings: IFeMeshSettings | Gets interface for working with FE mesh settings. |
| `Calculate` | Type: LoadingType, No: c_int | Errors: ErrorInfo[] | Calculates results of selected load and returns list of errors occurred during the calculation. |
| `CalculateAll` | – | Errors: ErrorInfo[] | Calculates results of all loads and modules and returns list of errors occurred during the calculation. |
| `CalculateApp` | – | Errors: ErrorInfo[] | Calculates results of the main application without modules and returns list of errors occurred during the calculation. |
| `CalculateModules` | – | Errors: ErrorInfo[] | Calculates results of all modules and returns list of errors occurred during the calculation. |
| `CalculateBatch` | Loadings: Loading[]* | Errors: ErrorInfo[] | Calculates results of selected loadings and returns list of errors occurred during the calculation. |
| `CalculateAsync` | Type: LoadingType, No: c_int | – | Asynchronous start of the calculation for selected load. |
| `CalculateAsyncAll` | – | – | Asynchronous start of the application and all modules calculation. |
| `CalculateAsyncApp` | – | – | Asynchronous start of the application calculation. Modules are not calculated. |
| `CalculateAsyncModules` | – | – | Starts calculation of all modules. End of calculation is indicated by calling event function rsCalculatationFinished. |
| `CalculateAsyncBatch` | Loadings: Loading[]* | – | Calculates results of selected loadings and returns list of errors occurred during the calculation. |
| `GetResultsInRasterPoints` | Type: LoadingType, No: c_int | Results: IResults | Gets results interface of specified loading. Results are in grid points. |
| `GetResultsInFeNodes` | Type: LoadingType, No: c_int | Results: IResults | Gets results interface of specified loading. Results are in FE mesh nodes |
| `Clean` | – | – | Deletes all results. |
| `ExportIsolines` | – | Isolines: IIsolines | Gets interface for working with isolines. |
| `GetSubCombinations` | – | SubCombinations: ISubCombinations | Gets interface for working with sub-combinations. |

### ICalculation2

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetMemberDivisions` | No: c_int | Divisions: c_double[] | Gets member divisions for results. |

### IComment

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Comment: Comment | Gets comment parameters. |
| `SetData` | Comment: Comment* | – | Sets comment parameters. |
| `Delete` | – | – | Deletes comment. |

### IComponentSurface

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetExtraData` | – | Surface: ComponentSurface | Gets component surface parameters. |
| `SetExtraData` | Surface: ComponentSurface* | – | Sets component surface parameters. |

### ICompoundSolid

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetExtraData` | – | Solid: CompoundSolid | Gets compound solid parameters. |
| `SetExtraData` | Solid: CompoundSolid* | – | Sets compound solid parameters. |

### IConnectionEccentricity

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Eccentricity: ConnectionEccentricity | Gets connection eccentricity parameters. |
| `SetData` | Eccentricity: ConnectionEccentricity* | – | Sets connection eccentricity parameters. |
| `Delete` | – | – | Deletes connection eccentricity. |

### IConnectionOfTwoMembers

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Connection: ConnectionOfTwoMembers | Gets connection of two members parameters. |
| `SetData` | Connection: ConnectionOfTwoMembers* | – | Sets connection of two members parameters. |
| `Delete` | – | – | Deletes connection of two members. |

### IContactSolid

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetExtraData` | – | Solid: ContactSolid | Gets contact solid parameters. |
| `SetExtraData` | Solid: ContactSolid* | – | Sets contact solid parameters. |

### ICoordinateSystem

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | CS: CoordinateSystem | Gets coordinate system parameters. |
| `GetNormal` | – | Normal: Point3D | Gets normal vector. |
| `LocalToGlobal` | Local: Point3D* | Global: Point3D | Converts local point to global point. |
| `GlobalToLocal` | Global: Point3D* | Local: Point3D | Converts global point to local point. |

### ICrossSection

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | CrossSection: CrossSection | Gets cross-section parameters. |
| `SetData` | CrossSection: CrossSection* | – | Sets cross-section parameters. |
| `Delete` | – | – | Deletes cross-section. |
| `GetDatabaseCrossSection` | – | Database: IUnknown | Gets interface for working with database cross-section. |

### IDimension

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Dimension: Dimension | Gets dimension parameters. |
| `Delete` | – | – | Deletes dimension. |

### IExportImport

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `Export` | Model: IUnknown*, Parameters: BSTR | Output: BSTR | Exports data. |
| `Import` | Model: IUnknown*, Parameters: BSTR | Output: BSTR | Imports data. |

### IExternalCommand

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `Execute` | Model: IUnknown*, Params: BSTR | – | Executes an external command |

### IFeMesh

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetNodes` | – | Nodes: FeMeshNode[] | Gets array of all FE mesh nodes. |
| `Get1DElements` | – | Elements: FeMesh1DElement[] | Gets array of all 1D finite elements. |
| `Get2DElements` | – | Elements: FeMesh2DElement[] | Gets array of all 2D finite elements (cells). |
| `Get3DElements` | – | Elements: FeMesh3DElement[] | Gets array of all 3D finite elements (bricks). |
| `GetMemberNodes` | No: c_int, At: ItemAt | Nodes: FeMeshNode[] | Gets array of FE mesh nodes for a specified member. |
| `GetMemberElements` | No: c_int, At: ItemAt | Elements: FeMesh1DElement[] | Gets array of FE mesh 1D finite elements for a specified member. |
| `GetSurfaceNodes` | No: c_int, At: ItemAt | Nodes: FeMeshNode[] | Gets array of FE mesh nodes for a specified surface. |
| `GetSurfaceElements` | No: c_int, At: ItemAt | Elements: FeMesh2DElement[] | Gets array of FE mesh 2D finite elements (cells) for a specified surface. |
| `GetSolidNodes` | No: c_int, At: ItemAt | Nodes: FeMeshNode[] | Gets array of FE mesh nodes for a specified solid. |
| `GetSolidElements` | No: c_int, At: ItemAt | Elements: FeMesh3DElement[] | Gets array of FE mesh 3D finite elements (bricks) for a specified solid. |
| `FindNodeNo` | Location: Point3D* | No: c_int | Finds number of a FE mesh node with specified coordinates. |

### IFeMeshRefinement

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Refinement: FeMeshRefinement | Gets FE-Mesh refinement parameters. |
| `SetData` | Refinement: FeMeshRefinement* | – | Sets FE-Mesh refinement parameters. |
| `Delete` | – | – | Deletes FE-Mesh refinement. |

### IFeMeshSettings

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetGeneral` | – | Settings: FeMeshGeneralSettings | Gets FE mesh general settings. |
| `SetGeneral` | Settings: FeMeshGeneralSettings* | – | Sets FE mesh general settings. |
| `GetMembers` | – | Settings: FeMeshMembersSettings | Gets FE mesh members settings. |
| `SetMembers` | Settings: FeMeshMembersSettings* | – | Sets FE mesh members settings. |
| `GetSurfaces` | – | Settings: FeMeshSurfacesSettings | Gets FE mesh surfaces settings. |
| `SetSurfaces` | Settings: FeMeshSurfacesSettings* | – | Sets FE mesh surfaces settings. |
| `GetSolids` | – | Settings: FeMeshSolidsSettings | Gets FE mesh solids settings. |
| `SetSolids` | Settings: FeMeshSolidsSettings* | – | Sets FE mesh solids settings. |

### IFreeCircularLoad

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Load: FreeCircularLoad | Gets free circular load parameters. |
| `SetData` | Load: FreeCircularLoad* | – | Sets free circular load parameters. |
| `Delete` | – | – | Deletes free circular load. |

### IFreeConcentratedLoad

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Load: FreeConcentratedLoad | Gets free concentrated load parameters. |
| `SetData` | Load: FreeConcentratedLoad* | – | Sets free concentrated load parameters. |
| `Delete` | – | – | Deletes free concentrated load. |

### IFreeLineLoad

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Load: FreeLineLoad | Gets free line load parameters. |
| `SetData` | Load: FreeLineLoad* | – | Sets free line load parameters. |
| `Delete` | – | – | Deletes free line load. |

### IFreePolygonLoad

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Load: FreePolygonLoad | Gets free polygon load parameters. |
| `SetData` | Load: FreePolygonLoad* | – | Sets free polygon load parameters. |
| `Delete` | – | – | Deletes free polygon load. |

### IFreeRectangularLoad

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Load: FreeRectangularLoad | Gets free rectangular load parameters. |
| `SetData` | Load: FreeRectangularLoad* | – | Sets free rectangular load parameters. |
| `Delete` | – | – | Deletes free rectangular load. |

### IFriction

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Friction: Friction | Gets friction parameters. |
| `SetData` | Friction: Friction* | – | Sets friction parameters. |

### IGasSolid

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetExtraData` | – | Solid: GasSolid | Gets gas solid parameters. |
| `SetExtraData` | Solid: GasSolid* | – | Sets gas solid parameters. |

### IGuideObjects

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `PrepareModification` | – | – | Prepares application for data modification. |
| `FinishModification` | – | – | Finishes data modification and updates the model. |
| `CancelModification` | – | – | Cancels current data modification. |
| `Clean` | – | – | Cleans guide objects. |
| `DeleteObjects` | Type: GuideObjectType, List: BSTR | – | Deletes specified objects. |
| `SetObjectID` | Type: GuideObjectType, No: c_int, At: ItemAt, ID: BSTR | – | Sets ID of the object. |
| `GetDimensionCount` | – | Count: c_int | Gets count of dimensions. |
| `GetDimension` | No: c_int, At: ItemAt | Dimension: IDimension | Gets interface for working with dimension. |
| `GetDimensions` | – | Dimensions: Dimension[] | Gets array of dimensions. |
| `GetLinearDimensionCount` | – | Count: c_int | Gets count of linear dimensions. |
| `GetLinearDimension` | No: c_int, At: ItemAt | Dimension: ILinearDimension | Gets interface for working with linear dimension. |
| `SetLinearDimension` | Dimension: LinearDimension* | IDimension: ILinearDimension | Sets linear dimension and returns it's interface. |
| `GetLinearDimensions` | – | Dimensions: LinearDimension[] | Gets array of linear dimensions. |
| `SetLinearDimensions` | Dimensions: LinearDimension[]* | – | Sets array of linear dimensions. |
| `GetArcLengthDimensionCount` | – | Count: c_int | Gets count of arc length dimensions. |
| `GetArcLengthDimension` | No: c_int, At: ItemAt | Dimension: IArcLengthDimension | Gets interface for working with arc length dimension. |
| `SetArcLengthDimension` | Dimension: ArcLengthDimension* | IDimension: IArcLengthDimension | Sets arc length dimension and returns it's interface. |
| `GetArcLengthDimensions` | – | Dimensions: ArcLengthDimension[] | Gets array of arc length dimensions. |
| `SetArcLengthDimensions` | Dimensions: ArcLengthDimension[]* | – | Sets array of arc length dimensions. |
| `GetAngularDimensionCount` | – | Count: c_int | Gets count of angular dimensions. |
| `GetAngularDimension` | No: c_int, At: ItemAt | Dimension: IAngularDimension | Gets interface for working with angular dimension. |
| `SetAngularDimension` | Dimension: AngularDimension* | IDimension: IAngularDimension | Sets angular dimension and returns it's interface. |
| `GetAngularDimensions` | – | Dimensions: AngularDimension[] | Gets array of angular dimensions. |
| `SetAngularDimensions` | Dimensions: AngularDimension[]* | – | Sets array of angular dimensions. |
| `GetRadialDimensionCount` | – | Count: c_int | Gets count of radial dimensions. |
| `GetRadialDimension` | No: c_int, At: ItemAt | Dimension: IRadialDimension | Gets interface for working with radial dimension. |
| `SetRadialDimension` | Dimension: RadialDimension* | IDimension: IRadialDimension | Sets radial dimension and returns it's interface. |
| `GetRadialDimensions` | – | Dimensions: RadialDimension[] | Gets array of radial dimensions. |
| `SetRadialDimensions` | Dimensions: RadialDimension[]* | – | Sets array of radial dimensions. |
| `GetSlopeDimensionCount` | – | Count: c_int | Gets count of slope dimensions. |
| `GetSlopeDimension` | No: c_int, At: ItemAt | Dimension: ISlopeDimension | Gets interface for working with slope dimension. |
| `SetSlopeDimension` | Dimension: SlopeDimension* | IDimension: ISlopeDimension | Sets slope dimension and returns it's interface. |
| `GetSlopeDimensions` | – | Dimensions: SlopeDimension[] | Gets array of slope dimensions. |
| `SetSlopeDimensions` | Dimensions: SlopeDimension[]* | – | Sets array of slope dimensions. |
| `GetHeightDimensionCount` | – | Count: c_int | Gets count of height dimensions. |
| `GetHeightDimension` | No: c_int, At: ItemAt | Dimension: IHeightDimension | Gets interface for working with height dimension. |
| `SetHeightDimension` | Dimension: HeightDimension* | IDimension: IHeightDimension | Sets height dimension and returns it's interface. |
| `GetHeightDimensions` | – | Dimensions: HeightDimension[] | Gets array of height dimensions. |
| `SetHeightDimensions` | Dimensions: HeightDimension[]* | – | Sets array of height dimensions. |
| `GetDimensionOptions` | Options: DimensionOptions* | – | Gets dimension options. |
| `SetDimensionOptions` | – | Options: DimensionOptions | Sets dimension options. |
| `GetCommentCount` | – | Count: c_int | Gets count of comments. |
| `GetComment` | No: c_int, At: ItemAt | Comment: IComment | Gets interface to Comment. |
| `SetComment` | Comment: Comment* | IComment: IComment | Sets comment and returns it's interface. |
| `GetComments` | – | Comments: Comment[] | Gets array of comments. |
| `SetComments` | Comments: Comment[]* | – | Sets array of comments. |
| `GetCoordinateSystemCount` | – | Count: c_int | Gets count of user-defined coordinate systems. |
| `GetCoordinateSystem` | No: c_int, At: ItemAt | UserCS: IUserCoordinateSystem | Gets interface for working with user-defined coordinate system. |
| `SetCoordinateSystem` | UserCS: UserCoordinateSystem* | IUserCS: IUserCoordinateSystem | Sets user-defined coordinate system and returns it's interface. |
| `GetCoordinateSystems` | – | UserCSs: UserCoordinateSystem[] | Gets array of user-defined coordinate systems. |
| `SetCoordinateSystems` | UserCSs: UserCoordinateSystem[]* | – | Sets array of user-defined coordinate systems. |
| `GetActiveCoordinateSystem` | – | No: c_int | Gets active coordinate system. |
| `SetActiveCoordinateSystem` | No: c_int, At: ItemAt | – | Sets active coordinate system. |
| `GetGuidelineCount` | – | Count: c_int | Gets count of guideline. |
| `GetGuideline` | No: c_int, At: ItemAt | Guideline: IGuideline | Gets interface for working with guideline. |
| `SetGuideline` | Guideline: Guideline* | IGuideline: IGuideline | Sets guideline and returns it's interface. |
| `GetGuidelines` | – | Guidelines: Guideline[] | Gets array of guidelines. |
| `SetGuidelines` | Guidelines: Guideline[]* | – | Sets array of guidelines. |

### IGuideline

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Guideline: Guideline | Gets guideline parameters. |
| `SetData` | Guideline: Guideline* | – | Sets guideline parameters. |
| `Delete` | – | – | Deletes guideline. |

### IHeightDimension

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Dimension: HeightDimension | Gets height dimension. |
| `SetData` | Dimension: HeightDimension* | – | Sets height dimension parameters. |
| `Delete` | – | – | Deletes height dimension. |

### IImperfection

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Load: Imperfection | Gets imperfection parameters. |
| `SetData` | Load: Imperfection* | – | Sets imperfection parameters. |
| `Delete` | – | – | Deletes imperfection. |

### IImposedLineDisplacement

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Load: ImposedLineDisplacement | Gets imposed line displacement parameters. |
| `SetData` | Load: ImposedLineDisplacement* | – | Sets imposed line displacement parameters. |
| `Delete` | – | – | Deletes imposed line deformation. |

### IImposedNodalDeformation

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Load: ImposedNodalDeformation | Gets imposed nodal deformation parameters. |
| `SetData` | Load: ImposedNodalDeformation* | – | Sets imposed nodal deformation parameters. |
| `Delete` | – | – | Deletes imposed nodal deformation. |

### IInternalCommand

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `Execute` | Command: BSTR | Result: BSTR | Executes an internal command |

### IIntersectionOfSurfaces

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Intersection: IntersectionOfSurfaces | Gets intersection of surfaces parameters. |
| `SetData` | Intersection: IntersectionOfSurfaces* | – | Sets intersection of surfaces parameters. |
| `Delete` | – | – | Deletes intersection of surfaces. |

### IIsolines

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetLayerCount` | – | Count: c_int | Gets count of layers. |
| `GetLayers` | – | Layers: IsolineLayer[] | Gets array of layers. |
| `GetArcCount` | – | Count: c_int | Gets count of arcs. |
| `GetArcs` | – | Arcs: IsolineArc[] | Gets array of arcs. |
| `GetCircleCount` | – | Count: c_int | Gets count of circles. |
| `GetCircles` | – | Circles: IsolineCircle[] | Gets array of circles. |
| `GetLineCount` | – | Count: c_int | Gets count of lines. |
| `GetLines` | – | Lines: IsolineLine[] | Gets array of lines. |
| `GetPointCount` | – | Count: c_int | Gets count of points. |
| `GetPoints` | – | Points: IsolinePoint[] | Gets array of points. |
| `GetStyleCount` | – | Count: c_int | Gets count of styles. |
| `GetStyles` | – | Styles: IsolineStyle[] | Gets array of styles. |
| `GetTextCount` | – | Count: c_int | Gets count of texts. |
| `GetTexts` | – | Texts: IsolineText[] | Gets array of text. |

### ILine

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Line: Line | Gets line parameters. |
| `SetData` | Line: Line* | – | Sets line parameters. |
| `Delete` | – | – | Deletes line. |
| `GetLocalCoordinateSystem` | Param: c_double | CS: ICoordinateSystem | Gets line local coordinate system. |
| `GetPointOnLine` | Param: c_double | Point: Point3D | Gets 3D point on the line in global coordinate system. |

### ILineHinge

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Hinge: LineHinge | Gets line hinge parameters. |
| `SetData` | Hinge: LineHinge* | – | Sets line hinge parameters. |
| `Delete` | – | – | Deletes line hinge. |

### ILineLoad

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Load: LineLoad | Gets line load parameters. |
| `SetData` | Load: LineLoad* | – | Sets line load parameters. |
| `Delete` | – | – | Deletes line load. |

### ILineOnSurface

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetExtraData` | – | Line: LineOnSurface | Gets line on surface parameters. |
| `SetExtraData` | Line: LineOnSurface* | – | Sets line on surface parameters. |

### ILineRelease

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Release: LineRelease | Gets line release parameters. |
| `SetData` | Release: LineRelease* | – | Sets line release parameters. |
| `Delete` | – | – | Deletes line release. |

### ILineReleaseType

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Type: LineReleaseType | Gets line release type parameters. |
| `SetData` | Type: LineReleaseType* | – | Sets line release type parameters. |
| `Delete` | – | – | Deletes line release type. |
| `GetNonlinearity` | Direction: NonlinearityDirectionType | Nonlinearity: IUnknown | Gets interface for working with line release type nonlinearity. |

### ILineSupport

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Support: LineSupport | Gets line support parameters. |
| `SetData` | Support: LineSupport* | – | Sets line support parameters. |
| `Delete` | – | – | Deletes line support. |

### ILineSupport2

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Support: LineSupport2 | Gets line support parameters. |
| `SetData` | Support: LineSupport2* | – | Sets line support parameters. |
| `Delete` | – | – | Deletes line support. |
| `GetNonlinearity` | Direction: NonlinearityDirectionType | Nonlinearity: IUnknown | Gets interface for working with nodal support nonlinearity. |

### ILinearDimension

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Dimension: LinearDimension | Gets linear dimension parameters. |
| `SetData` | Dimension: LinearDimension* | – | Sets linear dimension parameters. |
| `Delete` | – | – | Deletes linear dimension. |

### ILoadCase

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `PrepareModification` | – | – | Prepares application for load modification. |
| `FinishModification` | CheckDuplicity: VARIANT_BOOL | – | Finishes load modification and updates the model. |
| `CancelModification` | – | – | Cancels current data modification. |
| `IgnoreErrors` | Ignore: VARIANT_BOOL | – | Ignores throwing exception while set values are invalid. |
| `EnableSelections` | Enable: VARIANT_BOOL | – | Allows you to work with selected loads only. |
| `SelectObjects` | Type: LoadObjectType, List: BSTR | – | Selects loads of specified type. |
| `GetLastObjectNo` | Type: LoadObjectType | No: c_int | Gets number of last load object. |
| `Clean` | – | – | Cleans load case. |
| `DeleteObjects` | Type: LoadObjectType, List: BSTR | – | Deletes specified loads. |
| `SetObjectID` | Type: LoadObjectType, No: c_int, At: ItemAt, ID: BSTR | – | Sets ID of the load. |
| `PlausibilityCheck` | – | Error: ErrorInfo, Check: VARIANT_BOOL | Checks validity of loads. |
| `HasResults` | – | HasResults: VARIANT_BOOL | Indicates that load case has any results. |
| `GetData` | – | LCase: LoadCase | Gets load case parameters. |
| `SetData` | LCase: LoadCase* | – | Sets load case parameters. |
| `Delete` | – | – | Deletes load case. |
| `GetAnalysisParameters` | – | Analysis: AnalysisParameters | Gets analysis parameters. |
| `SetAnalysisParameters` | Analysis: AnalysisParameters* | – | Sets analysis parameters. |
| `GetIncrementallyIncreasingLoading` | – | Loading: IncrementallyIncreasingLoading | Get incrementally increasing loading parameters |
| `SetIncrementallyIncreasingLoading` | Loading: IncrementallyIncreasingLoading* | – | Set incrementally increasing loading parameters |
| `GetNodalLoadCount` | – | Count: c_int | Gets count of nodal loads. |
| `GetNodalLoad` | No: c_int, At: ItemAt | Load: INodalLoad | Gets interface for working with nodal load. |
| `SetNodalLoad` | Load: NodalLoad* | ILoad: INodalLoad | Sets nodal load and returns it's interface. |
| `GetNodalLoads` | – | Loads: NodalLoad[] | Gets array of nodal loads. |
| `SetNodalLoads` | Loads: NodalLoad[]* | – | Sets array of nodal loads. |
| `GetMemberLoadCount` | – | Count: c_int | Gets count of member loads. |
| `GetMemberLoad` | No: c_int, At: ItemAt | Load: IMemberLoad | Gets interface for working with member load. |
| `SetMemberLoad` | Load: MemberLoad* | ILoad: IMemberLoad | Sets member load and returns it's interface. |
| `GetMemberLoads` | – | Loads: MemberLoad[] | Gets array of member loads. |
| `SetMemberLoads` | Loads: MemberLoad[]* | – | Sets array of member loads. |
| `GetLineLoadCount` | – | Count: c_int | Gets count of line loads. |
| `GetLineLoad` | No: c_int, At: ItemAt | Load: ILineLoad | Gets line load interface. |
| `SetLineLoad` | Load: LineLoad* | ILoad: ILineLoad | Sets line load and returns it's interface. |
| `GetLineLoads` | – | Loads: LineLoad[] | Gets array of line loads. |
| `SetLineLoads` | Loads: LineLoad[]* | – | Sets array of line loads. |
| `GetSurfaceLoadCount` | – | Count: c_int | Gets count of surface loads. |
| `GetSurfaceLoad` | No: c_int, At: ItemAt | Load: ISurfaceLoad | Gets surface load interface. |
| `SetSurfaceLoad` | Load: SurfaceLoad* | ILoad: ISurfaceLoad | Sets surface load and returns it's interface. |
| `GetSurfaceLoads` | – | Loads: SurfaceLoad[] | Gets array of surface loads. |
| `SetSurfaceLoads` | Loads: SurfaceLoad[]* | – | Sets array of surface loads. |
| `GetSolidLoadCount` | – | Count: c_int | Gets count of solid loads. |
| `GetSolidLoad` | No: c_int, At: ItemAt | Load: ISolidLoad | Gets interface for working with solid load. |
| `SetSolidLoad` | Load: SolidLoad* | ILoad: ISolidLoad | Sets solid load and returns it's interface. |
| `GetSolidLoads` | – | Loads: SolidLoad[] | Gets array of solid loads. |
| `SetSolidLoads` | Loads: SolidLoad[]* | – | Sets array of solid loads. |
| `GetFreeConcentratedLoadCount` | – | Count: c_int | Gets count of free concentrated loads. |
| `GetFreeConcentratedLoad` | No: c_int, At: ItemAt | Load: IFreeConcentratedLoad | Gets interface for working with free concentrated load. |
| `SetFreeConcentratedLoad` | Load: FreeConcentratedLoad* | ILoad: IFreeConcentratedLoad | Sets free concentrated load and returns it's interface. |
| `GetFreeConcentratedLoads` | – | Loads: FreeConcentratedLoad[] | Gets array of free concentrated loads. |
| `SetFreeConcentratedLoads` | Loads: FreeConcentratedLoad[]* | – | Sets array of free concentrated loads. |
| `GetFreeLineLoadCount` | – | Count: c_int | Gets count of free line loads. |
| `GetFreeLineLoad` | No: c_int, At: ItemAt | Load: IFreeLineLoad | Gets interface for working with free line load. |
| `SetFreeLineLoad` | Load: FreeLineLoad* | ILoad: IFreeLineLoad | Sets free line load and returns it's interface. |
| `GetFreeLineLoads` | – | Loads: FreeLineLoad[] | Gets array of free line loads. |
| `SetFreeLineLoads` | Loads: FreeLineLoad[]* | – | Sets array of free line loads. |
| `GetFreeRectangularLoadCount` | – | Count: c_int | Gets count of free rectangular loads. |
| `GetFreeRectangularLoad` | No: c_int, At: ItemAt | Load: IFreeRectangularLoad | Gets interface for working with free rectangular load. |
| `SetFreeRectangularLoad` | Load: FreeRectangularLoad* | ILoad: IFreeRectangularLoad | Sets free rectangular load and returns it's interface. |
| `GetFreeRectangularLoads` | – | Loads: FreeRectangularLoad[] | Gets array of free rectangular loads. |
| `SetFreeRectangularLoads` | Loads: FreeRectangularLoad[]* | – | Sets array of free rectangular loads. |
| `GetFreeCircularLoadCount` | – | Count: c_int | Gets count of free circular loads. |
| `GetFreeCircularLoad` | No: c_int, At: ItemAt | Load: IFreeCircularLoad | Gets free circular Load interface. |
| `SetFreeCircularLoad` | Load: FreeCircularLoad* | ILoad: IFreeCircularLoad | Sets free circular load and returns it's interface. |
| `GetFreeCircularLoads` | – | Loads: FreeCircularLoad[] | Gets array of free circular loads. |
| `SetFreeCircularLoads` | Loads: FreeCircularLoad[]* | – | Sets array of free circular loads. |
| `GetFreePolygonLoadCount` | – | Count: c_int | Gets count of free polygon loads. |
| `GetFreePolygonLoad` | No: c_int, At: ItemAt | Load: IFreePolygonLoad | Gets interface for working with free polygon load. |
| `SetFreePolygonLoad` | Load: FreePolygonLoad* | ILoad: IFreePolygonLoad | Sets free polygon load and returns it's interface. |
| `GetFreePolygonLoads` | – | Loads: FreePolygonLoad[] | Gets array of free polygon loads. |
| `SetFreePolygonLoads` | Loads: FreePolygonLoad[]* | – | Sets array of free polygon loads. |
| `GetImposedNodalDeformationCount` | – | Count: c_int | Gets count of imposed nodal deformations. |
| `GetImposedNodalDeformation` | No: c_int, At: ItemAt | Deformation: IImposedNodalDeformation | Gets interface to imposed nodal deformation. |
| `SetImposedNodalDeformation` | Deformation: ImposedNodalDeformation* | IDeformation: IImposedNodalDeformation | Sets imposed nodal deformation and returns it's interface. |
| `GetImposedNodalDeformations` | – | Deformations: ImposedNodalDeformation[] | Gets array of imposed nodal deformations. |
| `SetImposedNodalDeformations` | Deformations: ImposedNodalDeformation[]* | – | Sets array of imposed nodal deformations. |
| `GetImposedLineDisplacementCount` | – | Count: c_int | Gets count of imposed line displacements. |
| `GetImposedLineDisplacement` | No: c_int, At: ItemAt | Displacement: IImposedLineDisplacement | Gets interface for working with imposed line displacement. |
| `SetImposedLineDisplacement` | Displacement: ImposedLineDisplacement* | IDisplacement: IImposedLineDisplacement | Sets imposed line displacement and returns it's interface. |
| `GetImposedLineDisplacements` | – | Displacements: ImposedLineDisplacement[] | Gets array of imposed line displacements. |
| `SetImposedLineDisplacements` | Displacements: ImposedLineDisplacement[]* | – | Sets array of imposed line displacements. |
| `GetImperfectionCount` | – | Count: c_int | Gets count of imperfections. |
| `GetImperfection` | No: c_int, At: ItemAt | Imperfection: IImperfection | Gets imperfection interface. |
| `SetImperfection` | Imperfection: Imperfection* | IImperfection: IImperfection | Sets imperfection and returns it's interface. |
| `GetImperfections` | – | Imperfections: Imperfection[] | Gets array of imperfections. |
| `SetImperfections` | Imperfections: Imperfection[]* | – | Sets array of imperfections. |

### ILoadCombination

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Combination: LoadCombination | Gets load combination parameters. |
| `SetData` | Combination: LoadCombination* | – | Sets load combination parameters. |
| `Delete` | – | – | Deletes load combination. |
| `HasResults` | – | HasResults: VARIANT_BOOL | Indicates if load combination has any results. |
| `GetAnalysisParameters` | – | Analysis: AnalysisParameters | Gets analysis parameters. |
| `SetAnalysisParameters` | Analysis: AnalysisParameters* | – | Sets analysis parameters. |
| `GetIncrementallyIncreasingLoading` | – | Loading: IncrementallyIncreasingLoading | Gets incrementally increasing loading parameters |
| `SetIncrementallyIncreasingLoading` | Loading: IncrementallyIncreasingLoading* | – | Sets incrementally increasing loading parameters |
| `GetLoadings` | – | Loadings: CombinationLoading[] | Gets list of loadings in the load combination. |
| `SetLoadings` | Loadings: CombinationLoading[]* | – | Sets list of loadings in load combination. |

### ILoads

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `PrepareModification` | – | – | Prepares modification. |
| `FinishModification` | – | – | Finishes modification. |
| `CancelModification` | – | – | Cancels current data modification. |
| `HasAnyResults` | – | HasResults: VARIANT_BOOL | Indicates if the model has any results. |
| `HasAnyLoadingResults` | Type: LoadingType | HasResults: VARIANT_BOOL | Indicates if at least one load of the specified loading type has any results. |
| `HasLoadingResults` | Loading: Loading | HasResults: VARIANT_BOOL |  |
| `Clean` | – | – | Deletes all loadings. |
| `DeleteLoading` | Type: LoadingType, List: BSTR | – | Deletes specified loadings. |
| `GetLastObjectNo` | Type: LoadingType | No: c_int | Gets number of last loading object. |
| `GetLoadCaseCount` | – | Count: c_int | Gets count of load cases. |
| `GetLoadCase` | No: c_int, At: ItemAt | Load: ILoadCase | Gets interface for working with load case. |
| `SetLoadCase` | Load: LoadCase* | ILoad: ILoadCase | Sets load case and returns it's interface. |
| `GetLoadCases` | – | Loads: LoadCase[] | Gets array of load cases. |
| `SetLoadCases` | Loads: LoadCase[]* | – | Sets array of load cases. |
| `GetLoadCombinationCount` | – | Count: c_int | Gets count of load combinations. |
| `GetLoadCombination` | No: c_int, At: ItemAt | Load: ILoadCombination | Gets interface for working with load combination. |
| `SetLoadCombination` | Load: LoadCombination* | ILoad: ILoadCombination | Sets load combination and returns it's interface. |
| `GetLoadCombinations` | – | Loads: LoadCombination[] | Gets array of load combinations. |
| `SetLoadCombinations` | Loads: LoadCombination[]* | – | Sets array of load combinations. |
| `GetResultCombinationCount` | – | Count: c_int | Gets count of result combinations. |
| `GetResultCombination` | No: c_int, At: ItemAt | Load: IResultCombination | Gets to result combination interface. |
| `SetResultCombination` | Load: ResultCombination* | ILoad: IResultCombination | Sets result combination and returns it's interface. |
| `GetResultCombinations` | – | Loads: ResultCombination[] | Gets array of result combinations. |
| `SetResultCombinations` | Loads: ResultCombination[]* | – | Sets array of result combinations. |
| `GetSuperCombinationCount` | – | Count: c_int | Gets count of super combinations. |
| `GetSuperCombination` | No: c_int, At: ItemAt | Load: ISuperCombination | Gets to super combination interface. |
| `SetSuperCombination` | Load: SuperCombination* | ILoad: ISuperCombination | Sets super combination and returns it's interface. |
| `GetSuperCombinations` | – | Loads: SuperCombination[] | Gets array of super combinations. |
| `SetSuperCombinations` | Loads: SuperCombination[]* | – | Sets array of super combinations. |
| `GenerateAreaLoad` | Area: AreaLoad* | – | Generates member loads from an area load of plane. |

### IMaterial

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Material: Material | Gets material parameters. |
| `SetData` | Material: Material* | – | Sets material parameters. |
| `Delete` | – | – | Deletes material. |
| `GetDatabaseMaterial` | – | Database: IUnknown | Gets interface for working with database material. |
| `GetModel` | – | Model: IUnknown | Gets interface for working with material model. |

### IMaterialIsotropicMasonry2DModel

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Data: MaterialIsotropicMasonry2DModel | Gets material isotropic masonry 2D model parameters. |
| `SetData` | Data: MaterialIsotropicMasonry2DModel* | – | Sets material isotropic masonry 2D model parameters. |

### IMaterialIsotropicModel

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Data: MaterialIsotropicModel | Gets material isotropic model parameters. |
| `SetData` | Data: MaterialIsotropicModel* | – | Sets material isotropic model parameters. |
| `GetDiagram` | – | Diagram: NonlinearityDiagram | Gets material stress-strain diagram. |
| `SetDiagram` | Diagram: NonlinearityDiagram* | – | Sets material stress-strain diagram. |

### IMaterialIsotropicThermalElasticModel

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Data: MaterialIsotropicThermalElasticModel | Gets material isotropic thermal-elastic model parameters. |
| `SetData` | Data: MaterialIsotropicThermalElasticModel* | – | Sets material isotropic thermal-elastic model parameters. |

### IMaterialOrthotropicElasticModel

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Data: MaterialOrthotropicElasticModel | Gets material orthotropic elastic model parameters. |
| `SetData` | Data: MaterialOrthotropicElasticModel* | – | Sets material orthotropic elastic model parameters. |

### IMaterialOrthotropicPlasticModel

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Data: MaterialOrthotropicPlasticModel | Gets material orthotropic plastic model parameters. |
| `SetData` | Data: MaterialOrthotropicPlasticModel* | – | Sets material orthotropic plastic model parameters. |

### IMember

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Member: Member | Gets member parameters. |
| `SetData` | Member: Member* | – | Sets member parameters. |
| `Delete` | – | – | Deletes member. |
| `GetExtraData` | – | Data: IUnknown | Returns interface for working with extra data depending on member type. |
| `GetLocalCoordinateSystem` | Param: c_double | CS: ICoordinateSystem | Gets member local coordinate system. |
| `GetEccentricity` | Param: c_double, LocalCS: VARIANT_BOOL | Eccentricity: Point3D | Gets member eccentricity. |
| `GetEffectiveLengths` | – | EffectiveLengths: MemberEffectiveLengths | Gets member effective lengths. |
| `SetEffectiveLengths` | EffectiveLengths: MemberEffectiveLengths* | – | Sets member effective lengths. |
| `GetStiffnessFactors` | – | Factors: MemberStiffnessFactors | Gets member stiffness factors. |
| `SetStiffnessFactors` | Factors: MemberStiffnessFactors* | – | Sets member stiffness factors. |

### IMemberDivision

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Division: MemberDivision | Gets member division parameters. |
| `SetData` | Division: MemberDivision* | – | Sets member division parameters. |
| `Delete` | – | – | Deletes member division. |

### IMemberEccentricity

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Eccentricity: MemberEccentricity | Gets member eccentricity parameters. |
| `SetData` | Eccentricity: MemberEccentricity* | – | Sets member eccentricity parameters. |
| `Delete` | – | – | Deletes member eccentricity. |

### IMemberElasticFoundation

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Foundation: MemberElasticFoundation | Gets member elastic foundation parameters. |
| `SetData` | Foundation: MemberElasticFoundation* | – | Sets member elastic foundation parameters. |
| `Delete` | – | – | Deletes member elastic foundation. |

### IMemberHinge

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Hinge: MemberHinge | Gets member hinge parameters. |
| `SetData` | Hinge: MemberHinge* | – | Sets member hinge parameters. |
| `Delete` | – | – | Deletes member hinge. |
| `GetNonlinearity` | Direction: NonlinearityDirectionType | Nonlinearity: IUnknown | Gets interface for working with member hinge nonlinearity. |

### IMemberLoad

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Load: MemberLoad | Gets member load parameters. |
| `SetData` | Load: MemberLoad* | – | Sets member load parameters. |
| `Delete` | – | – | Deletes member load. |

### IMemberNonlinearity

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Nonlinearity: MemberNonlinearity | Gets member nonlinearity parameters. |
| `SetData` | Nonlinearity: MemberNonlinearity* | – | Sets member nonlinearity parameters. |
| `Delete` | – | – | Deletes member nonlinearity. |

### IModel

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetApplication` | – | Application: IApplication | Gets interface for working with application. |
| `GetName` | – | Name: BSTR | Gets model name. |
| `SetName` | Name: BSTR | – | Sets model name. |
| `GetDescription` | – | Description: BSTR | Gets model description. |
| `SetDescription` | Description: BSTR | – | Sets model description. |
| `GetComment` | – | Comment: BSTR | Gets model comment. |
| `SetComment` | Comment: BSTR | – | Sets model comment. |
| `GetID` | – | ID: BSTR | Gets model ID. |
| `SetID` | ID: BSTR | – | Sets model ID. |
| `GetPath` | – | Path: BSTR | Gets the path to the current model file. |
| `GetTempFolderPath` | – | Path: BSTR | Gets the path to the folder where the model has it's temporary data. |
| `Save` | Path: BSTR | – | Saves model. |
| `Close` | – | – | Closes the model. |
| `Activate` | – | – | Activates the model. |
| `SetModified` | – | – | Sets the model as modified. |
| `Clean` | – | – | Cleans all model objects. |
| `GetProjectName` | – | Name: BSTR | Gets the project name. |
| `GetProjectDescription` | – | Description: BSTR | Gets the project description. |
| `GetProjectPath` | – | Path: BSTR | Gets the path to the project folder. |
| `GetGlobalZAxisOrientation` | – | Orientation: OrientationType | Gets positive orientation of global Z-axis. |
| `SetGlobalZAxisOrientation` | Orientation: OrientationType, Recalculate: VARIANT_BOOL | – | Sets positive orientation of global Z-axis. |
| `GetLocalZAxisOrientation` | – | Orientation: OrientationType | Gets orientation of local z-axis. |
| `SetLocalZAxisOrientation` | Orientation: OrientationType | – | Sets orientation of local z-axis. |
| `GetModelData` | – | Data: IModelData | Gets interface for working with model data. |
| `GetLoads` | – | Loads: ILoads | Gets interface for working with loads. |
| `GetCalculation` | – | Calculation: ICalculation | Gets interface for working with calculation. |
| `GetGuideObjects` | – | GuideObjects: IGuideObjects | Gets interface for working with guide objects. |
| `GetActiveView` | – | View: IView | Gets interface for working with active view. |
| `GetModule` | ModuleName: BSTR | Module: IUnknown | Gets the module interface based on its name. |
| `GetWorkPlane` | – | Plane: WorkPlane | Gets work plane parameters. |
| `SetWorkPlane` | Plane: WorkPlane* | – | Sets work plane parameters. |
| `GetGrid` | – | Grid: Grid | Gets grid parameters. |
| `SetGrid` | Grid: Grid* | – | Sets grid parameters. |
| `GetProtocols` | – | Protocols: IProtocols | Gets interface for working with printout reports. |

### IModel2

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetAverageRegions` | – | Regions: IAverageRegions | Gets interface for working with average regions. |

### IModel3

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetSections` | – | Sections: ISections | Gets interface for working with sections. |
| `GetFormulaParameters` | – | FormulaParameters: FormulaParameter[] | Gets array of formula parameters. |
| `SetFormulaParameters` | FormulaParameters: FormulaParameter[]* | – | Sets array of formula parameters. |
| `CleanFormulaParameters` | – | – | Cleans formula parameters. |

### IModelData

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetType` | – | Type: ModelType | Gets type of model. |
| `SetType` | Type: ModelType | – | Sets type of model. |
| `PrepareModification` | – | – | Prepares application for data modification. |
| `FinishModification` | CheckDuplicity: VARIANT_BOOL | – | Finishes data modification and updates the model. |
| `CancelModification` | – | – | Cancels current data modification. |
| `IgnoreErrors` | Ignore: VARIANT_BOOL | – | Ignores throwing exception while set values are invalid. |
| `EnableSelections` | Enable: VARIANT_BOOL | – | Allows you to work with selected objects only. |
| `SelectObjects` | Type: ModelObjectType, List: BSTR | – | Selects objects of specified type. |
| `ConnectMembers` | MemberList: BSTR | – | Connects specified members. |
| `ConnectLines` | LineList: BSTR | – | Connects specified lines. |
| `ConnectAll` | LineList: BSTR, MemberList: BSTR, SurfaceList: BSTR | – | Connects specified objects. |
| `MoveSelectedObjects` | Vector: Point3D* | – | Moves selected objects. |
| `CopySelectedObjects` | Copy: ManipulationCopy* | – | Copies selected objects. |
| `RotateSelectedObjects` | Rotate: ManipulationRotate* | – | Rotates and/or copies selected objects. |
| `MirrorSelectedObjects` | Mirror: ManipulationMirror* | – | Mirrors and/or copies selected objects. |
| `ProjectSelectedObjects` | Project: ManipulationProject* | – | Projects and/or copies selected objects. |
| `ScaleSelectedObjects` | Scale: ManipulationScale* | – | Scales selected objects with a factor. |
| `ShearSelectedObjects` | Shear: ManipulationShear* | – | Shears selected objects via angle. |
| `GetLastObjectNo` | Type: ModelObjectType | No: c_int | Gets number of last object. |
| `Clean` | – | – | Cleans model data. |
| `DeleteObjects` | Type: ModelObjectType, List: BSTR | – | Deletes specified objects. |
| `SetObjectID` | Type: ModelObjectType, No: c_int, At: ItemAt, ID: BSTR | – | Sets ID of the object. |
| `PlausibilityCheck` | – | Error: ErrorInfo, Check: VARIANT_BOOL | Checks validity of model data. |
| `GetIdenticalNodes` | Tolerance: c_double | Groups: BSTR[] | Gets array of identical nodes in the model. |
| `CorrectIdenticalNodes` | Correction: IdenticalObjectsCorrectionType, Tolerance: c_double, Group: BSTR | – | Corrects identical nodes in the model. |
| `GetMaterialDatabase` | – | Database: IUnknown | Gets interface for working with material database. |
| `GetCrossSectionDatabase` | – | Database: IUnknown | Gets interface for working with cross-section database. |
| `GetNodeCount` | – | Count: c_int | Gets count of nodes. |
| `GetNode` | No: c_int, At: ItemAt | Node: INode | Gets interface for working with node. |
| `SetNode` | Node: Node* | INode: INode | Sets node and returns it's interface. |
| `GetNodes` | – | Nodes: Node[] | Gets array of nodes. |
| `SetNodes` | Nodes: Node[]* | – | Sets array of nodes. |
| `GetLineCount` | – | Count: c_int | Gets count of lines. |
| `GetLine` | No: c_int, At: ItemAt | Line: ILine | Gets interface for working with line. |
| `SetLine` | Line: Line* | ILine: ILine | Sets line and returns it's interface. |
| `GetLines` | – | Lines: Line[] | Gets array of lines. |
| `SetLines` | Lines: Line[]* | – | Sets array of lines. |
| `GetTrajectoryLineCount` | – | Count: c_int | Gets count of trajectory lines. |
| `GetTrajectoryLine` | No: c_int, At: ItemAt | Line: ITrajectoryLine | Gets interface for working with trajectory line. |
| `SetTrajectoryLine` | Line: TrajectoryLine* | ILine: ITrajectoryLine | Sets trajectory line and returns it's interface. |
| `GetTrajectoryLines` | – | Lines: TrajectoryLine[] | Gets array of trajectory lines. |
| `SetTrajectoryLines` | Lines: TrajectoryLine[]* | – | Sets array of trajectory lines. |
| `GetLineOnSurfaceCount` | – | Count: c_int | Gets count of lines on surface. |
| `GetLineOnSurface` | No: c_int, At: ItemAt | Line: ILineOnSurface | Gets interface for working with line on surface. |
| `SetLineOnSurface` | Line: LineOnSurface* | ILine: ILineOnSurface | Sets line on surface and returns it's interface. |
| `GetLinesOnSurface` | – | Lines: LineOnSurface[] | Gets array of lines on surface. |
| `SetLinesOnSurface` | Lines: LineOnSurface[]* | – | Sets array of lines on surface. |
| `GetParabolaCount` | – | Count: c_int | Gets count of parabolas. |
| `GetParabola` | No: c_int, At: ItemAt | Line: IParabola | Gets interface for working with parabola. |
| `SetParabola` | Line: Parabola* | ILine: IParabola | Sets parabola and returns it's interface. |
| `GetParabolas` | – | Lines: Parabola[] | Gets array of parabolas. |
| `SetParabolas` | Lines: Parabola[]* | – | Sets array of parabolas. |
| `GetNurbSplineCount` | – | Count: c_int | Gets count of NurbSpline. |
| `GetNurbSpline` | No: c_int, At: ItemAt | Line: INurbSpline | Gets interface for working with NurbSpline. |
| `SetNurbSpline` | Line: NurbSpline* | ILine: INurbSpline | Sets NurbSpline and returns it's interface. |
| `GetNurbSplines` | – | Lines: NurbSpline[] | Gets array of NurbSpline. |
| `SetNurbSplines` | Lines: NurbSpline[]* | – | Sets array of NurbSplines. |
| `GetMaterialCount` | – | Count: c_int | Gets the count of materials. |
| `GetMaterial` | No: c_int, At: ItemAt | Material: IMaterial | Gets interface for working with material. |
| `SetMaterial` | Material: Material* | IMaterial: IMaterial | Sets material and returns it's interface. |
| `GetMaterials` | – | Materials: Material[] | Gets array of materials. |
| `SetMaterials` | Materials: Material[]* | – | Sets array of materials. |
| `GetSurfaceCount` | – | Count: c_int | Gets count of surfaces. |
| `GetSurface` | No: c_int, At: ItemAt | Surface: ISurface | Gets interface for working with surface. |
| `SetSurface` | Surface: Surface* | ISurface: ISurface | Sets surface and returns it's interface. |
| `GetSurfaces` | – | Surfaces: Surface[] | Gets array of surfaces. |
| `SetSurfaces` | Surfaces: Surface[]* | – | Sets array of surfaces. |
| `GetPlaneSurfaceCount` | – | Count: c_int | Gets count of plane surfaces. |
| `GetPlaneSurface` | No: c_int, At: ItemAt | Surface: ISurface | Gets interface for working with plane surface. |
| `SetPlaneSurface` | Surface: Surface* | ISurface: ISurface | Sets plane surface and returns it's interface. |
| `GetPlaneSurfaces` | – | Surfaces: Surface[] | Gets array of plane surfaces. |
| `SetPlaneSurfaces` | Surfaces: Surface[]* | – | Sets array of plane surfaces. |
| `GetQuadrangleSurfaceCount` | – | Count: c_int | Gets count of quadrangle surfaces. |
| `GetQuadrangleSurface` | No: c_int, At: ItemAt | Surface: ISurface | Gets interface for working with quadrangle surface. |
| `SetQuadrangleSurface` | Surface: Surface* | ISurface: ISurface | Sets quadrangle surface and returns it's interface. |
| `GetQuadrangleSurfaces` | – | Surfaces: Surface[] | Gets array of quadrangle surfaces. |
| `SetQuadrangleSurfaces` | Surfaces: Surface[]* | – | Sets array of quadrangle surfaces. |
| `GetBSplineSurfaceCount` | – | Count: c_int | Gets count of B-Spline surfaces. |
| `GetBSplineSurface` | No: c_int, At: ItemAt | Surface: IBSplineSurface | Gets interface for working with B-Spline surface. |
| `SetBSplineSurface` | Surface: BSplineSurface* | ISurface: IBSplineSurface | Sets B-Spline surface and returns it's interface. |
| `GetBSplineSurfaces` | – | Surfaces: BSplineSurface[] | Gets array of B-Spline surfaces. |
| `SetBSplineSurfaces` | Surfaces: BSplineSurface[]* | – | Sets array of B-Spline Surfaces. |
| `GetRotatedSurfaceCount` | – | Count: c_int | Gets count of rotated surfaces. |
| `GetRotatedSurface` | No: c_int, At: ItemAt | Surface: IRotatedSurface | Gets interface for working with rotated surface. |
| `SetRotatedSurface` | Surface: RotatedSurface* | ISurface: IRotatedSurface | Sets rotated surface and returns it's interface. |
| `GetRotatedSurfaces` | – | Surfaces: RotatedSurface[] | Gets array of rotated surfaces. |
| `SetRotatedSurfaces` | Surfaces: RotatedSurface[]* | – | Sets array of rotated surfaces. |
| `GetPipeSurfaceCount` | – | Count: c_int | Gets count of pipe surfaces. |
| `GetPipeSurface` | No: c_int, At: ItemAt | Surface: IPipeSurface | Gets interface to pipe surface. |
| `SetPipeSurface` | Surface: PipeSurface* | ISurface: IPipeSurface | Sets pipe surface and returns it's interface. |
| `GetPipeSurfaces` | – | Surfaces: PipeSurface[] | Gets array of pipe surfaces. |
| `SetPipeSurfaces` | Surfaces: PipeSurface[]* | – | Sets array of pipes. |
| `GetTrajectorySurfaceCount` | – | Count: c_int | Gets count of trajectory surfaces. |
| `GetTrajectorySurface` | No: c_int, At: ItemAt | Surface: ITrajectorySurface | Gets interface for working with trajectory surface. |
| `SetTrajectorySurface` | Surface: TrajectorySurface* | ISurface: ITrajectorySurface | Sets trajectory surface and returns it's interface. |
| `GetTrajectorySurfaces` | – | Surfaces: TrajectorySurface[] | Gets array of trajectory surfaces. |
| `SetTrajectorySurfaces` | Surfaces: TrajectorySurface[]* | – | Sets array of trajectory surfaces. |
| `GetNurbsSurfaceCount` | – | Count: c_int | Gets count of NURBS surfaces. |
| `GetNurbsSurface` | No: c_int, At: ItemAt | Surface: INurbsSurface | Gets interface for working with NURBS surface. |
| `SetNurbsSurface` | Surface: NurbsSurface* | ISurface: INurbsSurface | Sets NURBS surface and returns it's interface. |
| `GetNurbsSurfaces` | – | Surfaces: NurbsSurface[] | Gets array of NURBS surfaces. |
| `SetNurbsSurfaces` | Surfaces: NurbsSurface[]* | – | Sets array of NURBS surfaces. |
| `GetComponentSurfaceCount` | – | Count: c_int | Gets count of component surfaces. |
| `GetComponentSurface` | No: c_int, At: ItemAt | Surface: IComponentSurface | Gets interface for working with component surface. |
| `SetComponentSurface` | Surface: ComponentSurface* | ISurface: IComponentSurface | Sets component surface and returns it's interface. |
| `GetComponentSurfaces` | – | Surfaces: ComponentSurface[] | Gets array of component surfaces. |
| `SetComponentSurfaces` | Surfaces: ComponentSurface[]* | – | Sets array of component surfaces. |
| `GetSolidCount` | – | Count: c_int | Gets count of solids. |
| `GetSolid` | No: c_int, At: ItemAt | Solid: ISolid | Gets interface for working with solid. |
| `SetSolid` | Solid: Solid* | ISolid: ISolid | Sets solid and returns it's interface. |
| `GetSolids` | – | Solids: Solid[] | Gets array of solids. |
| `SetSolids` | Solids: Solid[]* | – | Sets array of solids. |
| `GetMaterialSolidCount` | – | Count: c_int | Gets count of material solids. |
| `GetMaterialSolids` | – | Solids: Solid[] | Gets array of material solids. |
| `GetGasSolidCount` | – | Count: c_int | Gets count of gas solids. |
| `GetGasSolid` | No: c_int, At: ItemAt | Solid: IGasSolid | Gets interface for working with gas solid. |
| `SetGasSolid` | Solid: GasSolid* | ISolid: IGasSolid | Sets gas solid and returns it's interface. |
| `GetGasSolids` | – | Solids: GasSolid[] | Gets array of gas solids. |
| `SetGasSolids` | Solids: GasSolid[]* | – | Sets array of gas solids. |
| `GetContactSolidCount` | – | Count: c_int | Gets count of contact solids. |
| `GetContactSolid` | No: c_int, At: ItemAt | Solid: IContactSolid | Gets interface for working with contact solid. |
| `SetContactSolid` | Solid: ContactSolid* | ISolid: IContactSolid | Sets contact solid and returns it's interface. |
| `GetContactSolids` | – | Solids: ContactSolid[] | Gets array of contact solids. |
| `SetContactSolids` | Solids: ContactSolid[]* | – | Sets array of contact solids. |
| `GetNullSolidCount` | – | Count: c_int | Gets count of null solids. |
| `GetNullSolids` | – | Solids: Solid[] | Gets array of null solids. |
| `GetCompoundSolidCount` | – | Count: c_int | Gets count of compound solids. |
| `GetCompoundSolid` | No: c_int, At: ItemAt | Solid: ICompoundSolid | Gets interface for working with compound solid. |
| `SetCompoundSolid` | Solid: CompoundSolid* | ISolid: ICompoundSolid | Sets compound solid and returns it's interface. |
| `GetCompoundSolids` | – | Solids: CompoundSolid[] | Gets array of compound solids. |
| `SetCompoundSolids` | Solids: CompoundSolid[]* | – | Sets array of compound solids. |
| `GetOpeningCount` | – | Count: c_int | Gets count of openings. |
| `GetOpening` | No: c_int, At: ItemAt | Opening: IOpening | Gets interface for working with opening. |
| `SetOpening` | Opening: Opening* | IOpening: IOpening | Sets opening and returns it's interface. |
| `GetOpenings` | – | Openings: Opening[] | Gets array of openings. |
| `SetOpenings` | Openings: Opening[]* | – | Sets array of openings. |
| `GetNodalSupportCount` | – | Count: c_int | Gets the count of nodal supports. |
| `GetNodalSupport` | No: c_int, At: ItemAt | Support: INodalSupport | Gets interface for working with nodal support. |
| `SetNodalSupport` | Support: NodalSupport* | ISupport: INodalSupport | Sets nodal support and returns it's interface. |
| `GetNodalSupports` | – | Supports: NodalSupport[] | Gets array of nodal supports. |
| `SetNodalSupports` | Supports: NodalSupport[]* | – | Sets array of nodal supports. |
| `GetLineSupportCount` | – | Count: c_int | Gets the count of line supports. |
| `GetLineSupport` | No: c_int, At: ItemAt | Support: ILineSupport | Gets interface for working with line support. |
| `SetLineSupport` | Support: LineSupport* | ISupport: ILineSupport | Sets line support and returns it's interface. |
| `GetLineSupports` | – | Supports: LineSupport[] | Gets array of line supports. |
| `SetLineSupports` | Supports: LineSupport[]* | – | Sets array of line supports. |
| `GetSurfaceSupportCount` | – | Count: c_int | Gets the count of surface supports. |
| `GetSurfaceSupport` | No: c_int, At: ItemAt | Support: ISurfaceSupport | Gets interface for working with surface support. |
| `SetSurfaceSupport` | Support: SurfaceSupport* | ISupport: ISurfaceSupport | Sets surface support and returns it's interface. |
| `GetSurfaceSupports` | – | Supports: SurfaceSupport[] | Gets array of surface supports. |
| `SetSurfaceSupports` | Supports: SurfaceSupport[]* | – | Sets array of surface supports. |
| `GetLineHingeCount` | – | Count: c_int | Gets the count of line hinge. |
| `GetLineHinge` | No: c_int, At: ItemAt | Hinge: ILineHinge | Gets interface for working with line hinge. |
| `SetLineHinge` | Hinge: LineHinge* | IHinge: ILineHinge | Sets line hinge and returns it's interface. |
| `GetLineHinges` | – | Hinges: LineHinge[] | Gets array of line hinges. |
| `SetLineHinges` | Hinges: LineHinge[]* | – | Sets array of line hinges. |
| `GetCrossSectionCount` | – | Count: c_int | Gets the count of cross-sections. |
| `GetCrossSection` | No: c_int, At: ItemAt | CrossSection: ICrossSection | Gets interface for working with cross-section. |
| `SetCrossSection` | CrossSection: CrossSection* | ICrossSection: ICrossSection | Sets cross-section and returns it's interface. |
| `GetCrossSections` | – | CrossSections: CrossSection[] | Gets array of cross-sections. |
| `SetCrossSections` | CrossSections: CrossSection[]* | – | Sets array of cross-sections. |
| `GetMemberHingeCount` | – | Count: c_int | Gets the count of member hinges. |
| `GetMemberHinge` | No: c_int, At: ItemAt | Hinge: IMemberHinge | Gets interface for working with member hinge. |
| `SetMemberHinge` | Hinge: MemberHinge* | IHinge: IMemberHinge | Sets member hinge and returns it's interface. |
| `GetMemberHinges` | – | Hinges: MemberHinge[] | Gets array of member hinges. |
| `SetMemberHinges` | Hinges: MemberHinge[]* | – | Sets array of member hinges. |
| `GetMemberEccentricityCount` | – | Count: c_int | Gets count of member eccentricities. |
| `GetMemberEccentricity` | No: c_int, At: ItemAt | Eccentricity: IMemberEccentricity | Gets interface for working with member eccentricity. |
| `SetMemberEccentricity` | Eccentricity: MemberEccentricity* | IEccentricity: IMemberEccentricity | Sets member eccentricity and returns it's interface. |
| `GetMemberEccentricities` | – | Eccentricities: MemberEccentricity[] | Gets array of member eccentricities. |
| `SetMemberEccentricities` | Eccentricities: MemberEccentricity[]* | – | Sets array of member eccentricities. |
| `GetMemberDivisionCount` | – | Count: c_int | Gets the count of member divisions. |
| `GetMemberDivision` | No: c_int, At: ItemAt | Division: IMemberDivision | Gets interface for working with member division. |
| `SetMemberDivision` | Division: MemberDivision* | IDivision: IMemberDivision | Sets member division and returns it's interface. |
| `GetMemberDivisions` | – | Divisions: MemberDivision[] | Gets array of member divisions. |
| `SetMemberDivisions` | Divisions: MemberDivision[]* | – | Sets array of member divisions. |
| `GetMemberCount` | – | Count: c_int | Gets count of members. |
| `GetMember` | No: c_int, At: ItemAt | Member: IMember | Gets interface for working with member. |
| `SetMember` | Member: Member* | IMember: IMember | Sets member and returns it's interface. |
| `GetMembers` | – | Members: Member[] | Gets array of members. |
| `SetMembers` | Members: Member[]* | – | Sets array of members. |
| `GetRibCount` | – | Count: c_int | Gets count of ribs. |
| `GetRib` | No: c_int, At: ItemAt | Rib: IRib | Gets interface for working with rib. |
| `SetRib` | Rib: Rib* | IRib: IRib | Sets rib and returns it's interface. |
| `GetRibs` | – | Ribs: Rib[] | Gets array of ribs. |
| `SetRibs` | Ribs: Rib[]* | – | Sets array of ribs. |
| `GetMemberElasticFoundationCount` | – | Count: c_int | Gets the count of member elastic foundations. |
| `GetMemberElasticFoundation` | No: c_int, At: ItemAt | Foundation: IMemberElasticFoundation | Gets interface for working with member elastic foundation. |
| `SetMemberElasticFoundation` | Foundation: MemberElasticFoundation* | IFoundation: IMemberElasticFoundation | Sets member elastic foundation and returns it's interface. |
| `GetMemberElasticFoundations` | – | Foundations: MemberElasticFoundation[] | Gets array of member elastic foundations. |
| `SetMemberElasticFoundations` | Foundations: MemberElasticFoundation[]* | – | Sets array of member elastic foundations. |
| `GetMemberNonlinearityCount` | – | Count: c_int | Gets the count of member nonlinearities. |
| `GetMemberNonlinearity` | No: c_int, At: ItemAt | Nonlinearity: IMemberNonlinearity | Gets interface for working with member nonlinearity. |
| `SetMemberNonlinearity` | Nonlinearity: MemberNonlinearity* | INonlinearity: IMemberNonlinearity | Sets member nonlinearity and returns it's interface. |
| `GetMemberNonlinearities` | – | Nonlinearities: MemberNonlinearity[] | Gets array of member nonlinearities. |
| `SetMemberNonlinearities` | Nonlinearities: MemberNonlinearity[]* | – | Sets array of member nonlinearities. |
| `GetSetOfMembersCount` | – | Count: c_int | Gets the count of sets of members. |
| `GetSetOfMembers` | No: c_int, At: ItemAt | Set: ISetOfMembers | Gets interface for working with set of members. |
| `SetSetOfMembers` | Set: SetOfMembers* | ISet: ISetOfMembers | Sets set of members and returns it's interface. |
| `GetSetsOfMembers` | – | Sets: SetOfMembers[] | Gets array of sets of members. |
| `SetSetsOfMembers` | Sets: SetOfMembers[]* | – | Sets array of sets of members. |
| `GetIntersectionOfSurfacesCount` | – | Count: c_int | Gets the count of intersections of surfaces. |
| `GetIntersectionOfSurfaces` | No: c_int, At: ItemAt | Intersection: IIntersectionOfSurfaces | Gets interface to intersection. |
| `SetIntersectionOfSurfaces` | Intersection: IntersectionOfSurfaces* | IIntersection: IIntersectionOfSurfaces | Sets intersection of surfaces and returns it's interface. |
| `GetIntersectionsOfSurfaces` | – | Intersections: IntersectionOfSurfaces[] | Gets array of intersections of surfaces. |
| `SetIntersectionsOfSurfaces` | Intersections: IntersectionOfSurfaces[]* | – | Sets array of intersections of surfaces. |
| `GetFeMeshRefinementCount` | – | Count: c_int | Gets the count of FE-Mesh refinements. |
| `GetFeMeshRefinement` | No: c_int, At: ItemAt | Refinement: IFeMeshRefinement | Gets interface for working with FE-Mesh refinement. |
| `SetFeMeshRefinement` | Refinement: FeMeshRefinement* | IRefinement: IFeMeshRefinement | Sets FE-Mesh refinement and returns it's interface. |
| `GetFeMeshRefinements` | – | Refinements: FeMeshRefinement[] | Gets array of FE-Mesh refinements. |
| `SetFeMeshRefinements` | Refinements: FeMeshRefinement[]* | – | Sets array of FE-Mesh refinements. |
| `GetNodalReleaseCount` | – | Count: c_int | Gets the count of nodal releases. |
| `GetNodalRelease` | No: c_int, At: ItemAt | Release: INodalRelease | Gets interface for working with nodal release. |
| `SetNodalRelease` | Release: NodalRelease* | IRelease: INodalRelease | Sets nodal release and returns it's interface. |
| `GetNodalReleases` | – | Releases: NodalRelease[] | Gets array of nodal releases. |
| `SetNodalReleases` | Releases: NodalRelease[]* | – | Sets array of nodal releases. |
| `GetLineReleaseTypeCount` | – | Count: c_int | Gets the count of line releases type. |
| `GetLineReleaseType` | No: c_int, At: ItemAt | Type: ILineReleaseType | Gets interface for working with line release type. |
| `SetLineReleaseType` | Type: LineReleaseType* | IType: ILineReleaseType | Sets line release type and returns it's interface. |
| `GetLineReleaseTypes` | – | Types: LineReleaseType[] | Gets array of line release types. |
| `SetLineReleaseTypes` | Types: LineReleaseType[]* | – | Sets array of line release types. |
| `GetLineReleaseCount` | – | Count: c_int | Gets the count of line releases. |
| `GetLineRelease` | No: c_int, At: ItemAt | Release: ILineRelease | Gets interface for working with line release. |
| `SetLineRelease` | Release: LineRelease* | IRelease: ILineRelease | Sets line release and returns it's interface. |
| `GetLineReleases` | – | Releases: LineRelease[] | Gets array of line releases. |
| `SetLineReleases` | Releases: LineRelease[]* | – | Sets array of line releases. |
| `GetConnectionEccentricityCount` | – | Count: c_int | Gets count of connection eccentricities. |
| `GetConnectionEccentricity` | No: c_int, At: ItemAt | Eccentricity: IConnectionEccentricity | Gets interface for working with connection eccentricity. |
| `SetConnectionEccentricity` | Eccentricity: ConnectionEccentricity* | IEccentricity: IConnectionEccentricity | Sets connection eccentricity and returns it's interface. |
| `GetConnectionEccentricities` | – | Eccentricities: ConnectionEccentricity[] | Gets array of connection eccentricities. |
| `SetConnectionEccentricities` | Eccentricities: ConnectionEccentricity[]* | – | Sets array of connection eccentricities. |
| `GetConnectionOfTwoMembersCount` | – | Count: c_int | Gets the count of connections of two members. |
| `GetConnectionOfTwoMembers` | No: c_int, At: ItemAt | Connection: IConnectionOfTwoMembers | Gets interface for working with connection of two members. |
| `SetConnectionOfTwoMembers` | Connection: ConnectionOfTwoMembers* | IConnection: IConnectionOfTwoMembers | Sets connection of two members and returns it's interface. |
| `GetConnectionsOfTwoMembers` | – | Connections: ConnectionOfTwoMembers[] | Gets array of connections of two members. |
| `SetConnectionsOfTwoMembers` | Connections: ConnectionOfTwoMembers[]* | – | Sets array of connections of two members. |
| `GetTendonCount` | – | Count: c_int | Gets count of tendons. |
| `GetTendon` | No: c_int, At: ItemAt | Tendon: ITendon | Gets interface for working with tendon. |
| `SetTendon` | Tendon: Tendon* | ITendon: ITendon | Sets tendon and returns it's interface. |
| `GetTendons` | – | Tendons: Tendon[] | Gets array of tendons. |
| `SetTendons` | Tendons: Tendon[]* | – | Sets array of tendons. |

### IModelData2

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetLineSupport2` | No: c_int, At: ItemAt | Support: ILineSupport2 | Gets interface for working with line support. |
| `SetLineSupport2` | Support: LineSupport2* | ISupport: ILineSupport2 | Sets line support and returns it's interface. |
| `GetLineSupports2` | – | Supports: LineSupport2[] | Gets array of line supports. |
| `SetLineSupports2` | Supports: LineSupport2[]* | – | Sets array of line supports. |

### INodalLoad

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Load: NodalLoad | Gets nodal load parameters. |
| `SetData` | Load: NodalLoad* | – | Sets nodal load parameters. |
| `Delete` | – | – | Deletes nodal load. |

### INodalRelease

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Release: NodalRelease | Gets nodal release parameters. |
| `SetData` | Release: NodalRelease* | – | Sets nodal release parameters. |
| `Delete` | – | – | Deletes nodal release. |

### INodalSupport

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Support: NodalSupport | Gets nodal support parameters. |
| `SetData` | Support: NodalSupport* | – | Sets nodal support parameters. |
| `Delete` | – | – | Deletes nodal support. |
| `GetNonlinearity` | Direction: NonlinearityDirectionType | Nonlinearity: IUnknown | Gets interface for working with nodal support nonlinearity. |

### INode

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Node: Node | Gets node parameters. |
| `SetData` | Node: Node* | – | Sets node parameters. |
| `Delete` | – | – | Deletes node. |
| `SetCoorinateSystem` | CS: CoordinateSystemType | – | Sets the coordinate system. |

### INonlinearityDiagram

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Diagram: NonlinearityDiagram | Gets nonlinearity diagram parameters. |
| `SetData` | Diagram: NonlinearityDiagram* | – | Sets nonlinearity diagram parameters. |

### INotify

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `CalculationStatus` | – | Status: BSTR | Returns current calculation status. |
| `CalculationFinished` | – | Errors: ErrorInfo[] | Indicates that the calculation has been finished. |
| `Question` | Question: ErrorInfo* | Result: VARIANT_BOOL | Called when user interaction is needed. |

### INurbSpline

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetExtraData` | – | Line: NurbSpline | Gets NurbSpline parameters. |
| `SetExtraData` | Line: NurbSpline* | – | Sets NurbSpline parameters. |

### INurbsSurface

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetExtraData` | – | Surface: NurbsSurface | Gets NURBS surface parameters. |
| `SetExtraData` | Surface: NurbsSurface* | – | Sets NURBS surface parameters. |

### IOpening

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Opening: Opening | Gets opening parameters. |
| `SetData` | Opening: Opening* | – | Sets opening parameters. |
| `Delete` | – | – | Deletes opening including all boundary lines. |
| `DeleteWithLines` | – | – | Deletes opening without losing boundary lines. |

### IOrthotropicThickness

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Stiffness: SurfaceStiffness | Gets surface stiffness parameters. |
| `SetData` | Stiffness: SurfaceStiffness* | – | Sets surface stiffness parameters. |
| `GetStiffnessMatrix` | – | Matrix: StiffnessMatrix | Gets surface orthotropic stiffness matrix parameters. |
| `SetStiffnessMatrix` | Matrix: StiffnessMatrix* | – | Sets surface orthotropic stiffness matrix parameters. |
| `GetTransformedStiffnessMatrix` | – | Matrix: StiffnessMatrix | Gets surface transformed orthotropic stiffness matrix parameters. |

### IOrthotropicThickness2

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData2` | – | Stiffness: SurfaceStiffness2 | Gets surface stiffness parameters. |
| `SetData2` | Stiffness: SurfaceStiffness2* | – | Sets surface stiffness parameters. |

### IParabola

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetExtraData` | – | Line: Parabola | Gets parabola parameters. |
| `SetExtraData` | Line: Parabola* | – | Sets parabola parameters. |

### IPartialActivity

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Activity: PartialActivity | Gets partial activity parameters. |
| `SetData` | Activity: PartialActivity* | – | Sets partial activity parameters. |

### IPipeSurface

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetExtraData` | – | Surface: PipeSurface | Gets pipe parameters. |
| `SetExtraData` | Surface: PipeSurface* | – | Sets pipe parameters. |

### IPlasticHinge

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Hinge: PlasticHinge | Gets plastic hinge parameters. |
| `SetData` | Hinge: PlasticHinge* | – | Sets plastic hinge parameters. |

### IProtocol

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetHeaderOptions` | – | Options: ProtocolHeaderOptions | Gets options of the printout report displayed header. |
| `GetDate` | – | Date: ProtocolDate | Gets printout report date displayed in the header. |
| `GetNumbering` | – | Numbering: ProtocolNumbering | Gets page and sheet numbering. |
| `GetCompany` | – | Company: ProtocolCompany | Gets company information defined in the printout report. |

### IProtocols

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetProtocolCount` | – | Count: c_int | Gets count of all available printout reports in the model. |
| `GetProtocol` | No: c_int, At: ItemAt | Protocol: IProtocol | Gets the printout report interface at the specified index or with the specified No. |
| `GetProtocols` | – | Protocols: Protocol[] | Gets array of basic information about all available printout reports. |

### IRadialDimension

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Dimension: RadialDimension | Gets radial dimension parameters. |
| `SetData` | Dimension: RadialDimension* | – | Sets radial dimension parameters. |
| `Delete` | – | – | Deletes radial dimension. |

### IResultBeam

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Beam: ResultBeam | Gets result beam parameters. |
| `SetData` | Beam: ResultBeam* | – | Sets result beam parameters. |

### IResultCombination

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Combination: ResultCombination | Gets result combination parameters. |
| `SetData` | Combination: ResultCombination* | – | Sets result combination parameters. |
| `Delete` | – | – | Deletes result combination. |
| `HasResults` | – | HasResults: VARIANT_BOOL | Indicates if result combination has any results. |
| `GetQuadraticCombination` | – | Combination: QuadraticCombination | Gets quadratic combination parameters. |
| `SetQuadraticCombination` | Combination: QuadraticCombination* | – | Sets quadratic combination parameters. |
| `GetLoadings` | – | Loadings: CombinationLoading[] | Gets list of loadings in the result combination. |
| `SetLoadings` | Loadings: CombinationLoading[]* | – | Sets list of loadings in result combination. |

### IResults

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetCalculationTime` | – | Date: c_double | Gets date and time of the latest calculation. |
| `AddRibsToMembers` | Add: VARIANT_BOOL | – | On members addition of rib components. |
| `SubtractRibsFromSurfaces` | Subtract: VARIANT_BOOL | – | On surfaces subtraction of rib components. |
| `GetSummary` | – | Summary: SummaryResults | Gets summary results. |
| `GetMaximum` | – | Maximum: MaximumResults | Gets maximum results. |
| `GetNodalSupportForcesCount` | NodeNo: c_int, At: ItemAt, LocalCS: VARIANT_BOOL | Count: c_int | Gets count of nodal support forces. |
| `GetNodalSupportForces` | NodeNo: c_int, At: ItemAt, LocalCS: VARIANT_BOOL | Results: NodalSupportForces[] | Gets array of nodal support forces. |
| `GetNodalExtremeSupportForces` | NodeNo: c_int, At: ItemAt, LocalCS: VARIANT_BOOL | Results: NodalSupportForces[] | Gets array of extreme nodal support forces. |
| `GetAllNodalSupportForcesCount` | LocalCS: VARIANT_BOOL | Count: c_int | Gets count of all nodal support forces. |
| `GetAllNodalSupportForces` | LocalCS: VARIANT_BOOL | Results: NodalSupportForces[] | Gets array of nodal support forces in all supported nodes. |
| `GetAllNodalExtremeSupportForces` | LocalCS: VARIANT_BOOL | Results: NodalSupportForces[] | Gets array of extreme nodal support forces. |
| `GetNodalSummarySupportForces` | LocalCS: VARIANT_BOOL | Results: SummarySupportForces | Gets array of summary nodal support forces. |
| `GetNodalDeformationsCount` | NodeNo: c_int, At: ItemAt | Count: c_int | Gets nodal deformation count. |
| `GetNodalDeformations` | NodeNo: c_int, At: ItemAt | Results: NodalDeformations[] | Gets array of nodal deformations. |
| `GetAllNodalDeformationsCount` | – | Count: c_int | Gets count of all nodal deformations. |
| `GetAllNodalDeformations` | – | Results: NodalDeformations[] | Gets array of all nodal deformations. |
| `GetNodalExtremeDeformations` | – | Results: NodalDeformations[] | Gets array of nodal deformations extremes. |
| `GetLineSupportForcesCount` | LineNo: c_int, At: ItemAt, LocalCS: VARIANT_BOOL | Count: c_int | Gets count of line support forces. |
| `GetLineSupportForces` | LineNo: c_int, At: ItemAt, LocalCS: VARIANT_BOOL | Results: LineSupportForces[] | Gets array of line support forces. |
| `GetLineExtremeSupportForces` | LineNo: c_int, At: ItemAt, LocalCS: VARIANT_BOOL | Results: LineSupportForces[] | Gets array of extreme line support forces. |
| `GetLinesSupportForcesCount` | LocalCS: VARIANT_BOOL | Count: c_int | Gets count of all line support forces. |
| `GetLinesSupportForces` | LocalCS: VARIANT_BOOL | Results: LineSupportForces[] | Gets array of all line support forces. |
| `GetLinesExtremeSupportForces` | LocalCS: VARIANT_BOOL | Results: LineSupportForces[] | Gets array of extreme line support forces. |
| `GetLinesSummarySupportForces` | LocalCS: VARIANT_BOOL | Results: SummarySupportForces | Gets array of summary line support forces. |
| `GetMemberDeformationsCount` | MemberNo: c_int, At: ItemAt, Axes: MemberAxesType | Count: c_int | Gets count of member deformations. |
| `GetMemberDeformations` | MemberNo: c_int, At: ItemAt, Axes: MemberAxesType | Results: MemberDeformations[] | Gets array of member deformations. |
| `GetMemberExtremeDeformations` | MemberNo: c_int, At: ItemAt, Axes: MemberAxesType | Results: MemberDeformations[] | Gets array of member extreme deformations. |
| `GetMembersDeformationsCount` | Axes: MemberAxesType | Count: c_int | Gets count of all members deformations. |
| `GetMembersDeformations` | Axes: MemberAxesType | Results: MemberDeformations[] | Gets array of all members deformations. |
| `GetMembersExtremeDeformations` | Axes: MemberAxesType | Results: MemberDeformations[] | Gets array of all members extreme deformations. |
| `GetMemberInternalForcesCount` | MemberNo: c_int, At: ItemAt, MemberAxes: VARIANT_BOOL | Count: c_int | Gets count of member internal forces. |
| `GetMemberInternalForces` | MemberNo: c_int, At: ItemAt, MemberAxes: VARIANT_BOOL | Results: MemberForces[] | Gets array of member internal forces. |
| `GetMemberExtremeInternalForces` | MemberNo: c_int, At: ItemAt, MemberAxes: VARIANT_BOOL | Results: MemberForces[] | Gets array of member extreme internal forces. |
| `GetMembersInternalForcesCount` | MemberAxes: VARIANT_BOOL | Count: c_int | Gets count of all member internal forces. |
| `GetMembersInternalForces` | MemberAxes: VARIANT_BOOL | Results: MemberForces[] | Gets array of all members internal forces. |
| `GetMembersExtremeInternalForces` | MemberAxes: VARIANT_BOOL | Results: MemberForces[] | Gets array of all member extreme internal forces. |
| `GetMemberContactForcesCount` | MemberNo: c_int, At: ItemAt, MemberAxes: VARIANT_BOOL | Count: c_int | Gets count of member contact forces. |
| `GetMemberContactForces` | MemberNo: c_int, At: ItemAt, MemberAxes: VARIANT_BOOL | Results: MemberForces[] | Gets array of member contact forces. |
| `GetMemberExtremeContactForces` | MemberNo: c_int, At: ItemAt, MemberAxes: VARIANT_BOOL | Results: MemberForces[] | Gets array of member extreme contact forces. |
| `GetMembersContactForcesCount` | MemberAxes: VARIANT_BOOL | Count: c_int | Gets count of all member contact forces. |
| `GetMembersContactForces` | MemberAxes: VARIANT_BOOL | Results: MemberForces[] | Gets array of all member contact forces. |
| `GetMembersExtremeContactForces` | MemberAxes: VARIANT_BOOL | Results: MemberForces[] | Gets array of all member extreme contact forces. |
| `GetSetOfMembersInternalForcesCount` | SetNo: c_int, At: ItemAt, MemberAxes: VARIANT_BOOL | Count: c_int | Gets count of set of members internal forces. |
| `GetSetOfMembersInternalForces` | SetNo: c_int, At: ItemAt, MemberAxes: VARIANT_BOOL | Results: MemberForces[] | Gets array of set of members internal forces. |
| `GetSetOfMembersExtremeInternalForces` | SetNo: c_int, At: ItemAt, MemberAxes: VARIANT_BOOL | Results: MemberForces[] | Gets array of set of members extreme internal forces. |
| `GetSetsOfMembersInternalForcesCount` | MemberAxes: VARIANT_BOOL | Count: c_int | Gets count of all sets of members internal forces. |
| `GetSetsOfMembersInternalForces` | MemberAxes: VARIANT_BOOL | Results: MemberForces[] | Gets array of all sets of members internal forces. |
| `GetSetsOfMembersExtremeInternalForces` | MemberAxes: VARIANT_BOOL | Results: MemberForces[] | Gets array of all sets of members extreme internal forces. |
| `GetCrossSectionInternalForcesCount` | CrossSectionNo: c_int, At: ItemAt, MemberAxes: VARIANT_BOOL | Count: c_int | Gets count of cross-section internal forces. |
| `GetCrossSectionInternalForces` | CrossSectionNo: c_int, At: ItemAt, MemberAxes: VARIANT_BOOL | Results: MemberForces[] | Gets array of cross-section internal forces. |
| `GetCrossSectionExtremeInternalForces` | CrossSectionNo: c_int, At: ItemAt, MemberAxes: VARIANT_BOOL | Results: MemberForces[] | Gets array of cross-section extreme internal forces extremes. |
| `GetCrossSectionsInternalForcesCount` | MemberAxes: VARIANT_BOOL | Count: c_int | Gets count of all cross-sections internal forces. |
| `GetCrossSectionsInternalForces` | MemberAxes: VARIANT_BOOL | Results: MemberForces[] | Gets array of all cross-sections internal forces. |
| `GetCrossSectionsExtremeInternalForces` | MemberAxes: VARIANT_BOOL | Results: MemberForces[] | Gets array of all cross-sections extreme internal forces. |
| `GetSurfaceDeformationsCount` | SurfaceNo: c_int, At: ItemAt, LocalCS: VARIANT_BOOL | Count: c_int | Gets count of surface deformations. |
| `GetSurfaceDeformations` | SurfaceNo: c_int, At: ItemAt, LocalCS: VARIANT_BOOL | Results: SurfaceDeformations[] | Gets array of surface deformations. |
| `GetSurfacesDeformationsCount` | LocalCS: VARIANT_BOOL | Count: c_int | Gets count of all surfaces deformations. |
| `GetSurfacesDeformations` | LocalCS: VARIANT_BOOL | Results: SurfaceDeformations[] | Gets array of all surfaces deformations. |
| `GetSurfaceInternalForcesCount` | SurfaceNo: c_int, At: ItemAt | Count: c_int | Gets count of surface internal forces. |
| `GetSurfaceInternalForces` | SurfaceNo: c_int, At: ItemAt | Results: SurfaceInternalForces[] | Gets array of surface internal forces. |
| `GetSurfacesInternalForcesCount` | – | Count: c_int | Gets count of all surfaces internal forces. |
| `GetSurfacesInternalForces` | – | Results: SurfaceInternalForces[] | Gets array of all surfaces forces. |
| `GetSurfaceBasicStressesCount` | SurfaceNo: c_int, At: ItemAt | Count: c_int | Gets count of surface basic stresses. |
| `GetSurfaceBasicStresses` | SurfaceNo: c_int, At: ItemAt | Results: SurfaceBasicStresses[] | Gets array of surface basic stresses. |
| `GetSurfacesBasicStressesCount` | – | Count: c_int | Gets count of all surfaces basic stresses. |
| `GetSurfacesBasicStresses` | – | Results: SurfaceBasicStresses[] | Gets array of all surface basic stresses. |
| `GetSurfacePrincipalStressesCount` | SurfaceNo: c_int, At: ItemAt | Count: c_int | Gets count of surface principal stresses. |
| `GetSurfacePrincipalStresses` | SurfaceNo: c_int, At: ItemAt | Results: SurfacePrincipalStresses[] | Gets array of surface principal stresses. |
| `GetSurfacesPrincipalStressesCount` | – | Count: c_int | Gets count of all surfaces principal stresses. |
| `GetSurfacesPrincipalStresses` | – | Results: SurfacePrincipalStresses[] | Gets array of all surface principal stresses. |
| `GetSurfaceOtherStressesCount` | SurfaceNo: c_int, At: ItemAt | Count: c_int | Gets count of surface other stresses. |
| `GetSurfaceOtherStresses` | SurfaceNo: c_int, At: ItemAt | Results: SurfaceOtherStresses[] | Gets array of surface other stresses. |
| `GetSurfacesOtherStressesCount` | – | Count: c_int | Gets count of all surfaces other stresses. |
| `GetSurfacesOtherStresses` | – | Results: SurfaceOtherStresses[] | Gets array of all surface other stresses. |
| `GetSurfaceContactStressesCount` | SurfaceNo: c_int, At: ItemAt | Count: c_int | Gets count of surface contact stresses. |
| `GetSurfaceContactStresses` | SurfaceNo: c_int, At: ItemAt | Results: SurfaceContactStresses[] | Gets array of surface contact stresses. |
| `GetSurfacesContactStressesCount` | – | Count: c_int | Gets count of all surface contact stresses. |
| `GetSurfacesContactStresses` | – | Results: SurfaceContactStresses[] | Gets array of all surface contact stresses. |
| `GetSurfaceEquivalentStressesCount` | SurfaceNo: c_int, At: ItemAt | Count: c_int | Gets count of surface equivalent stresses. |
| `GetSurfaceEquivalentStresses` | SurfaceNo: c_int, At: ItemAt, Hypothesis: HypothesisType | Results: SurfaceEquivalentStresses[] | Gets array of surface equivalent stresses. |
| `GetSurfacesEquivalentStressesCount` | – | Count: c_int | Gets count of all surface equivalent stresses. |
| `GetSurfacesEquivalentStresses` | Hypothesis: HypothesisType | Results: SurfaceEquivalentStresses[] | Gets array of all surface equivalent stresses. |
| `GetSurfaceBasicStrainsCount` | SurfaceNo: c_int, At: ItemAt | Count: c_int | Gets count of surface basic strains. |
| `GetSurfaceBasicStrains` | SurfaceNo: c_int, At: ItemAt | Results: SurfaceBasicStrains[] | Gets array of surface basic strains. |
| `GetSurfacesBasicStrainsCount` | – | Count: c_int | Gets count of all surfaces basic strains. |
| `GetSurfacesBasicStrains` | – | Results: SurfaceBasicStrains[] | Gets array of all surfaces basic strains. |
| `GetSurfacePrincipalStrainsCount` | SurfaceNo: c_int, At: ItemAt | Count: c_int | Gets count of surface principal strains. |
| `GetSurfacePrincipalStrains` | SurfaceNo: c_int, At: ItemAt | Results: SurfacePrincipalStrains[] | Gets array of surface principal strains. |
| `GetSurfacesPrincipalStrainsCount` | – | Count: c_int | Gets count of all surfaces principal strains. |
| `GetSurfacesPrincipalStrains` | – | Results: SurfacePrincipalStrains[] | Gets array of all surfaces principal strains. |
| `GetSurfaceMaximumStrainsCount` | SurfaceNo: c_int, At: ItemAt | Count: c_int | Gets count of surface maximum strains. |
| `GetSurfaceMaximumStrains` | SurfaceNo: c_int, At: ItemAt | Results: SurfaceMaximumStrains[] | Gets array of surface maximum strains. |
| `GetSurfacesMaximumStrainsCount` | – | Count: c_int | Gets count of all surfaces maximum strains. |
| `GetSurfacesMaximumStrains` | – | Results: SurfaceMaximumStrains[] | Gets array of all surfaces maximum strains. |
| `GetSurfaceStrainsCount` | SurfaceNo: c_int, At: ItemAt | Count: c_int | Gets count of surface strains. |
| `GetSurfaceStrains` | SurfaceNo: c_int, At: ItemAt, Hypothesis: HypothesisType | Results: SurfaceStrains[] | Gets array of surface strains. |
| `GetSurfacesStrainsCount` | – | Count: c_int | Gets count of all surfaces strains. |
| `GetSurfacesStrains` | Hypothesis: HypothesisType | Results: SurfaceStrains[] | Gets array of all surfaces strains. |
| `GetSurfacePlasticStrainsCount` | SurfaceNo: c_int, At: ItemAt | Count: c_int | Gets count of surface plastic strains. |
| `GetSurfacePlasticStrains` | SurfaceNo: c_int, At: ItemAt | Results: SurfacePlasticStrains[] | Gets array of surface plastic strains. |
| `GetSurfacesPlasticStrainsCount` | – | Count: c_int | Gets count of all surfaces plastic strains. |
| `GetSurfacesPlasticStrains` | – | Results: SurfacePlasticStrains[] | Gets array of all surfaces plastic strains. |
| `GetSurfaceCrackStrainsCount` | SurfaceNo: c_int, At: ItemAt | Count: c_int | Gets count of surface crack strains. |
| `GetSurfaceCrackStrains` | SurfaceNo: c_int, At: ItemAt | Results: SurfaceCrackStrains[] | Gets array of surface crack strains. |
| `GetSurfacesCrackStrainsCount` | – | Count: c_int | Gets count of all surfaces crack strains. |
| `GetSurfacesCrackStrains` | – | Results: SurfaceCrackStrains[] | Gets array of all surfaces crack strains. |
| `GetSurfaceCriteriaCount` | SurfaceNo: c_int, At: ItemAt | Count: c_int | Gets count of surface criteria. |
| `GetSurfaceCriteria` | SurfaceNo: c_int, At: ItemAt | Results: SurfaceCriteria[] | Gets array of surface criteria. |
| `GetSurfacesCriteriaCount` | – | Count: c_int | Gets count of all surfaces criteria. |
| `GetSurfacesCriteria` | – | Results: SurfaceCriteria[] | Gets array of all surfaces criteria. |
| `GetSolidDeformationsCount` | SolidNo: c_int, At: ItemAt, LocalCS: VARIANT_BOOL | Count: c_int | Gets count of solid deformations. |
| `GetSolidDeformations` | SolidNo: c_int, At: ItemAt, LocalCS: VARIANT_BOOL | Results: SolidDeformations[] | Gets array of solid deformations. |
| `GetSolidsDeformationsCount` | LocalCS: VARIANT_BOOL | Count: c_int | Gets count of all solids deformations. |
| `GetSolidsDeformations` | LocalCS: VARIANT_BOOL | Results: SolidDeformations[] | Gets array of all solids deformations. |
| `GetSolidStressesCount` | SolidNo: c_int, At: ItemAt | Count: c_int | Gets count of solid stresses. |
| `GetSolidStresses` | SolidNo: c_int, At: ItemAt | Results: SolidStresses[] | Gets array of solid stresses. |
| `GetSolidsStressesCount` | – | Count: c_int | Gets count of all solids stresses. |
| `GetSolidsStresses` | – | Results: SolidStresses[] | Gets array of all solids stresses. |
| `GetSolidStrainsCount` | SolidNo: c_int, At: ItemAt | Count: c_int | Gets count of solid strains. |
| `GetSolidStrains` | SolidNo: c_int, At: ItemAt | Results: SolidStrains[] | Gets array of solid strains. |
| `GetSolidsStrainsCount` | – | Count: c_int | Gets count of all solids strains. |
| `GetSolidsStrains` | – | Results: SolidStrains[] | Gets array of all solids strains. |
| `GetSolidPlasticStrainsCount` | SolidNo: c_int, At: ItemAt | Count: c_int | Gets count of solid plastic strains. |
| `GetSolidPlasticStrains` | SolidNo: c_int, At: ItemAt | Results: SolidPlasticStrains[] | Gets array of solid plastic strains. |
| `GetSolidsPlasticStrainsCount` | – | Count: c_int | Gets count of all solids plastic strains. |
| `GetSolidsPlasticStrains` | – | Results: SolidPlasticStrains[] | Gets array of all solids plastic strains. |
| `GetSolidCriteriaCount` | SolidNo: c_int, At: ItemAt | Count: c_int | Gets count of solid criteria. |
| `GetSolidCriteria` | SolidNo: c_int, At: ItemAt | Results: SolidCriteria[] | Gets array of solid criteria. |
| `GetSolidsCriteriaCount` | – | Count: c_int | Gets count of all solids criteria. |
| `GetSolidsCriteria` | – | Results: SolidCriteria[] | Gets array of all solids criteria. |
| `GetSolidGasPressureCount` | SolidNo: c_int, At: ItemAt | Count: c_int | Gets count of solid gas pressure. |
| `GetSolidGasPressure` | SolidNo: c_int, At: ItemAt | Results: SolidGasPressure[] | Gets array of solid gas pressure. |
| `GetSolidsGasPressureCount` | – | Count: c_int | Gets count of all solids gas pressure. |
| `GetSolidsGasPressure` | – | Results: SolidGasPressure[] | Gets array of all solids gas pressure. |
| `GetSolidStressesAtCenterOfGravityCount` | SolidNo: c_int, At: ItemAt | Count: c_int | Gets count of solid stresses at center of gravity. |
| `GetSolidStressesAtCenterOfGravity` | SolidNo: c_int, At: ItemAt | Results: SolidStresses[] | Gets array of solid stresses at center of gravity of FE. |
| `GetSolidsStressesAtCenterOfGravityCount` | – | Count: c_int | Gets count of all solids stresses at center of gravity of FE. |
| `GetSolidsStressesAtCenterOfGravity` | – | Results: SolidStresses[] | Gets array of all solids stresses at center of gravity of FE. |
| `GetSolidStrainsAtCenterOfGravityCount` | SolidNo: c_int, At: ItemAt | Count: c_int | Gets count of solid strains of center of gravity. |
| `GetSolidStrainsAtCenterOfGravity` | SolidNo: c_int, At: ItemAt | Results: SolidStrains[] | Gets array of solid strains at center of gravity of FE. |
| `GetSolidsStrainsAtCenterOfGravityCount` | – | Count: c_int | Gets count of all solids strains at center of gravity of FE. |
| `GetSolidsStrainsAtCenterOfGravity` | – | Results: SolidStrains[] | Gets array of all solids strains at center of gravity of FE. |
| `GetSolidGasPressureCenterCount` | SolidNo: c_int, At: ItemAt | Count: c_int | Gets count of solid gas pressure center. |
| `GetSolidGasPressureCenter` | SolidNo: c_int, At: ItemAt | Results: SolidGasPressure[] | Gets array of solid gas pressure center. |
| `GetSolidsGasPressureCenterCount` | – | Count: c_int | Gets count of all solids gas pressure center. |
| `GetSolidsGasPressureCenter` | – | Results: SolidGasPressure[] | Gets array of all solids gas pressure center. |

### IResults2

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetResultsInSection` | SectionNo: c_int, At: ItemAt, ResultsType: ResultsType, DistributionType: ResultsDistributionType, FilterDuplicateValues: VARIANT_BOOL | Results: SectionResult[] | Gets results in defined section. |
| `GetResultant` | SectionNo: c_int, At: ItemAt, DistributionType: ResultsDistributionType | Resultant: ResultantForce | Gets resultant force in defined section. |

### IRib

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Rib: Rib | Gets rib parameters. |
| `SetData` | Rib: Rib* | – | Sets rib parameters. |
| `Delete` | – | – | Deletes rib. |
| `GetRibCrossSection` | End: VARIANT_BOOL | CrossSection: RibCrossSection | Gets rib cross-section. |

### IRotatedSurface

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetExtraData` | – | Surface: RotatedSurface | Gets rotated surface parameters. |
| `SetExtraData` | Surface: RotatedSurface* | – | Sets rotated surface parameters. |

### IScaffolding

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Scaffolding: Scaffolding | Gets scaffolding parameters. |
| `SetData` | Scaffolding: Scaffolding* | – | Sets scaffolding parameters. |

### IScaffoldingHinge

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetInnerTube` | – | Diagram: NonlinearityDiagram | Gets inner tube parameters. |
| `SetInnerTube` | Diagram: NonlinearityDiagram* | – | Sets inner tube parameters. |
| `GetOuterTube` | – | Diagram: NonlinearityDiagram | Gets outer tube parameters. |
| `SetOuterTube` | Diagram: NonlinearityDiagram* | – | Sets outer tube parameters. |

### ISection

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Section: Section | Gets section parameters. |
| `SetData` | Section: Section* | – | Sets section parameters. |
| `Delete` | – | – | Deletes section. |

### ISections

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `PrepareModification` | – | – | Prepares application for data modification. |
| `FinishModification` | – | – | Finishes data modification and updates the model. |
| `CancelModification` | – | – | Cancels current data modification. |
| `Clean` | – | – | Cleans sections objects. |
| `DeleteObjects` | List: BSTR | – | Deletes specified objects. |
| `SetObjectID` | No: c_int, At: ItemAt, ID: BSTR | – | Sets ID of the object. |
| `GetSectionCount` | – | Count: c_int | Gets count of sections. |
| `GetSection` | No: c_int, At: ItemAt | Section: ISection | Gets interface for working with section. |
| `SetSection` | Section: Section* | ISection: ISection | Sets section and returns it's interface. |
| `GetSections` | – | Sections: Section[] | Gets array of sections. |
| `SetSections` | Sections: Section[]* | – | Sets array of sections. |

### ISetOfMembers

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Set: SetOfMembers | Gets set of members parameters. |
| `SetData` | Set: SetOfMembers* | – | Sets set of members parameters. |
| `Delete` | – | – | Deletes set of members. |

### ISlopeDimension

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Dimension: SlopeDimension | Gets slope dimension. |
| `SetData` | Dimension: SlopeDimension* | – | Sets slope dimension parameters. |
| `Delete` | – | – | Deletes slope dimension. |

### ISolid

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Solid: Solid | Gets solid parameters. |
| `SetData` | Solid: Solid* | – | Sets solid parameters. |
| `Delete` | – | – | Deletes solid. |
| `GetAxes` | – | Axes: SolidAxes | Gets solid axes parameters. |
| `SetAxes` | Axes: SolidAxes* | – | Sets solid axes parameters. |

### ISolidLoad

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Load: SolidLoad | Gets solid load parameters. |
| `SetData` | Load: SolidLoad* | – | Sets solid load parameters. |
| `Delete` | – | – | Deletes solid load. |

### ISpringBeam

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Beam: SpringBeam | Gets spring beam parameters. |
| `SetData` | Beam: SpringBeam* | – | Sets spring beam parameters. |

### IStiffnessBeam

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Beam: StiffnessBeam | Gets stiffness beam parameters. |
| `SetData` | Beam: StiffnessBeam* | – | Sets stiffness beam parameters. |

### ISubCombinations

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `SetSubCombination` | CombinationNo: c_int, Definition: BSTR | – | Sets sub-combination parameters |
| `Clean` | – | – | Removes sub-combination |
| `Calculate` | – | Errors: ErrorInfo[] | Calculates results of defined sub-combination and returns list of errors occurred during the calculation. |
| `GetResultsInRasterPoints` | – | Results: IResults | Gets results interface. Results are in raster points. |
| `GetResultsInFeNodes` | – | Results: IResults | Gets results interface. Results are in FE mesh nodes |

### ISuperCombination

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Combination: SuperCombination | Gets super combination parameters. |
| `SetData` | Combination: SuperCombination* | – | Sets super combination parameters. |
| `Delete` | – | – | Deletes super combination. |
| `HasResults` | – | HasResults: VARIANT_BOOL | Indicates that super combination has any results. |
| `GetQuadraticCombination` | – | Combination: QuadraticCombination | Gets quadratic combination parameters. |
| `SetQuadraticCombination` | Combination: QuadraticCombination* | – | Sets quadratic combination parameters. |
| `GetLoadings` | – | Loadings: CombinationLoading[] | Gets list of loadings in the super combination. |
| `SetLoadings` | Loadings: CombinationLoading[]* | – | Sets list of loadings in super combination. |

### ISurface

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Surface: Surface | Gets surface parameters. |
| `SetData` | Surface: Surface* | – | Sets surface parameters. |
| `Delete` | – | – | Deletes surface. |
| `GetGrid` | – | Grid: SurfaceGrid | Gets surface grid parameters. |
| `SetGrid` | Grid: SurfaceGrid* | – | Sets surface grid parameters. |
| `GetInputAxes` | – | Axes: SurfaceAxes | Gets surface axes for input. |
| `SetInputAxes` | Axes: SurfaceAxes* | – | Sets surface axes for input. |
| `GetResultAxes` | – | Axes: SurfaceAxes | Gets surface axes for results. |
| `SetResultAxes` | Axes: SurfaceAxes* | – | Sets surface axes for results. |
| `GetLocalCoordinateSystem` | Point: Point3D* | CS: ICoordinateSystem | Gets surface local coordinate system. |
| `GetVariableThickness` | – | Thickness: IVariableThickness | Gets surface variable thickness. |
| `GetOrthotropicThickness` | – | Thickness: IOrthotropicThickness | Gets surface orthotropic thickness. |

### ISurfaceLoad

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Load: SurfaceLoad | Gets surface load parameters. |
| `SetData` | Load: SurfaceLoad* | – | Sets surface load parameters. |
| `Delete` | – | – | Deletes surface load. |

### ISurfaceSupport

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Support: SurfaceSupport | Gets surface support parameters. |
| `SetData` | Support: SurfaceSupport* | – | Sets surface support parameters. |
| `Delete` | – | – | Deletes surface support. |
| `GetNonlinearity` | Direction: NonlinearityDirectionType | Nonlinearity: IUnknown | Gets interface for working with surface support nonlinearity. |

### ISurfaceSupportNonlinearity

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | NL: SurfaceSupportNonlinearity | Gets surface support nonlinearity parameters. |
| `SetData` | NL: SurfaceSupportNonlinearity* | – | Sets surface support nonlinearity parameters. |

### ITendon

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Tendon: Tendon | Gets tendon basic parameters. |
| `SetData` | Tendon: Tendon* | – | Sets tendon basic parameters. |
| `GetMaterial` | – | Material: Material | Gets material parameters. |
| `SetMaterial` | Material: Material* | – | Sets material parameters. |
| `GetGeometry` | – | Points: Point3D[] | Gets array of 3D coordinates of tendon points. |
| `SetGeometry` | Points: Point3D[]* | – | Sets array of 3D coordinates of tendon points. |
| `GetSolverLoad` | – | SolverLoad: c_double[] | Gets array of solver load. |
| `SetSolverLoad` | SolverLoad: c_double[]* | – | Sets array of solver load. |
| `Delete` | – | – | Deletes tendon. |

### ITrajectoryLine

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetExtraData` | – | Line: TrajectoryLine | Gets trajectory line parameters. |
| `SetExtraData` | Line: TrajectoryLine* | – | Sets trajectory line parameters. |

### ITrajectorySurface

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetExtraData` | – | Surface: TrajectorySurface | Gets trajectory surface parameters. |
| `SetExtraData` | Surface: TrajectorySurface* | – | Sets trajectory surface parameters. |

### IUserCoordinateSystem

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | UserCS: UserCoordinateSystem | Gets coordinate system parameters. |
| `SetData` | UserCS: UserCoordinateSystem* | – | Sets coordinate system parameters. |
| `Delete` | – | – | Deletes coordinate system. |

### IVariableThickness

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `GetData` | – | Thickness: VariableThickness | Gets surface variable thickness parameters. |
| `SetData` | Thickness: VariableThickness* | – | Sets surface variable thickness parameters. |

### IView

| Methode | Eingabe | Ausgabe | Hilfetext |
|---|---|---|---|
| `PickObjects` | Tool: ToolType | Objects: BSTR | Start selection tool to select specified objects. |
| `CopyGraphicsToClipboard` | – | – | Copy graphics to clipboard. |
| `CleanClipboard` | – | – | Empty clipboard. |
| `GetViewPoint` | – | ViewPoint: ViewPoint | Gets view point. |
| `SetViewPoint` | ViewPoint: ViewPoint* | – | Sets viewpoint. |
| `SelectLoading` | Type: LoadingType, No: c_int | – | Selects loading. |
| `ShowLoads` | ShowLoads: VARIANT_BOOL, ShowValues: VARIANT_BOOL | – | Shows loads. |
| `ShowPerspective` | Show: VARIANT_BOOL | – | Shows perspective. |
| `ShowAll` | – | – | Shows All. |

## 2. Strukturen

- **AnalysisParameters**: `Loading` (Loading), `Method` (AnalysisMethodType), `SolvingSystemMethod` (SolvingSystemMethodType), `ModifyLoadingByFactor` (VARIANT_BOOL), `LoadingFactor` (c_double), `DivideResultsByFactor` (VARIANT_BOOL), `StiffnessFactorsMaterials` (VARIANT_BOOL), `StiffnessFactorsCrossSections` (VARIANT_BOOL), `StiffnessFactorsMembers` (VARIANT_BOOL), `ConsiderFavorableEffects` (VARIANT_BOOL), `ReferIF` (VARIANT_BOOL), `ReferIFForNormalForces` (VARIANT_BOOL), `ReferIFForShearForces` (VARIANT_BOOL), `ReferIFForMoments` (VARIANT_BOOL), `CalculateKinematicMechanism` (VARIANT_BOOL), `LoadIncrements` (c_int), `SaveResults` (VARIANT_BOOL), `SaveResultsIteration` (c_int)
- **AngularDimension**: `No` (c_int), `ID` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `ReferenceObjectType` (ModelObjectType), `ReferenceObjectNo` (c_int), `ObjectType` (ModelObjectType), `ObjectList` (BSTR), `Placement` (DimensionPlacement), `Offset` (c_double), `AngleGreater180` (VARIANT_BOOL), `Angles` (c_double[]), `Symbol` (BSTR)
- **ArcLengthDimension**: `No` (c_int), `ID` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `LineNo` (c_int), `NodeList` (BSTR), `Placement` (DimensionPlacement), `Offset` (c_double), `Lengths` (c_double[]), `Symbol` (BSTR)
- **AreaLoad**: `LoadCaseNo` (c_int), `Direction` (LoadDirectionType), `MemberLoadDirection` (DirectionType), `Application` (AreaLoadApplicationType), `DistributionType` (AreaLoadDistributionType), `Distribution` (LoadDistributionType), `Node1No` (c_int), `Magnitude1` (c_double), `Node2No` (c_int), `Magnitude2` (c_double), `Node3No` (c_int), `Magnitude3` (c_double), `LoadArray` (c_double[]), `CornerNodes` (BSTR), `InfluenceSingle` (BSTR), `InfluenceParallel` (BSTR)
- **AverageRegion**: `No` (c_int), `ID` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `IsGenerated` (VARIANT_BOOL), `Description` (BSTR), `SurfaceList` (BSTR), `AngularRotation` (c_double), `CenterPoint` (Point3D), `Form` (AverageRegionFormType), `Dimension1` (c_double), `Dimension2` (c_double), `DirectionUWithMx` (VARIANT_BOOL), `DirectionUWithMy` (VARIANT_BOOL), `DirectionUWithVx` (VARIANT_BOOL), `DirectionUWithVy` (VARIANT_BOOL), `DirectionUWithMxy` (VARIANT_BOOL), `DirectionUWithNxy` (VARIANT_BOOL), `DirectionUWithNx` (VARIANT_BOOL), `DirectionUWithNy` (VARIANT_BOOL), `DirectionVWithMx` (VARIANT_BOOL), `DirectionVWithMy` (VARIANT_BOOL), `DirectionVWithVx` (VARIANT_BOOL), `DirectionVWithVy` (VARIANT_BOOL), `DirectionVWithMxy` (VARIANT_BOOL), `DirectionVWithNxy` (VARIANT_BOOL), `DirectionVWithNx` (VARIANT_BOOL), `DirectionVWithNy` (VARIANT_BOOL), `Projection` (AverageRegionProjectionType), `ProjectionVector` (Point3D), `ResultValuesToZero` (VARIANT_BOOL), `DistributionOfInternalForces` (AverageRegionDistributionType)
- **BSplineSurface**: `General` (Surface), `MatrixOrder` (c_int), `SplineOrder` (c_int), `NodeList` (BSTR)
- **Buoyancy**: `UseAltitude` (VARIANT_BOOL), `Altitude` (c_double)
- **CalculationNonlinearities**: `SupportsAndElasticFoundations` (VARIANT_BOOL), `MembersDueToType` (VARIANT_BOOL), `Hinges` (VARIANT_BOOL), `MemberNonlinearities` (VARIANT_BOOL), `ContactSolids` (VARIANT_BOOL), `Materials` (VARIANT_BOOL), `ThermalElasticMaterials` (VARIANT_BOOL)
- **CalculationOptions**: `ShearStiffness` (VARIANT_BOOL), `LargeDeformationDivisions` (VARIANT_BOOL), `ModifyStiffness` (VARIANT_BOOL), `ConsiderExtraOptions` (VARIANT_BOOL), `IgnoreRotationDegreesOfFreedom` (VARIANT_BOOL), `CheckForcesAndMoments` (VARIANT_BOOL), `StressOnBeams` (VARIANT_BOOL), `NonsymmetricDirectSolver` (VARIANT_BOOL)
- **CalculationSettings**: `MaxIterations` (c_int), `LoadCaseIncrements` (c_int), `LoadCombinationIncrements` (c_int), `MaximumIncreasingLoading` (c_int), `MemberDivisionsForResultDiagram` (c_int), `SpecialMemberDivisions` (c_int), `MemberDivisionsForMaxMin` (c_int), `FeMeshSubdivisions` (c_int), `NewtonRaphsonPickard` (c_int), `DivisionForMembersWithNodes` (VARIANT_BOOL)
- **Column**: `Type` (ColumnType), `WidthX` (c_double), `WidthY` (c_double), `CrossSectionName` (BSTR), `Height` (c_double), `Model` (ColumnModelType), `MaterialNo` (c_int), `HeadConditions` (SupportConditionsType), `BaseConditions` (SupportConditionsType), `BaseElastic` (c_double), `ActivateShearStiffness` (VARIANT_BOOL)
- **CombinationLoading**: `No` (c_int), `Factor` (c_double), `Loading` (Loading), `Description` (BSTR), `Criterion` (CombinationCriterionType), `Group` (c_int), `Model` (BSTR)
- **Comment**: `No` (c_int), `ID` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `Text` (BSTR), `ObjectType` (CommentObjectType), `ObjectNo` (c_int), `Point` (Point3D), `Offset` (Point3D), `Frame` (CommentFrameType), `Rotation` (c_double)
- **ComponentSurface**: `General` (Surface), `Active` (VARIANT_BOOL), `ParentSurfaceNo` (c_int)
- **CompoundSolid**: `General` (Solid), `SolidList` (BSTR), `Operation` (CompoundSolidOperationType), `HideCutOffParts` (VARIANT_BOOL)
- **ConnectionEccentricity**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `IsGenerated` (VARIANT_BOOL), `ReferenceSystem` (ReferenceSystemType), `Eccentricity` (Point3D), `HorizontalAlignment` (HorizontalAlignmentType), `VerticalAlignment` (VerticalAlignmentType)
- **ConnectionOfTwoMembers**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `MainMemberNo` (c_int), `MainMemberSide` (ConnectionSideType), `MainMemberEccentricityNo` (c_int), `MainMemberHingeNo` (c_int), `ConnectedMemberNo` (c_int), `ConnectedMemberSide` (ConnectionSideType), `ConnectedMemberEccentricityNo` (c_int), `ConnectedMemberHingeNo` (c_int), `UnlockConnectedMember` (VARIANT_BOOL), `Deactivate` (VARIANT_BOOL), `GeneratedNodes` (BSTR), `GeneratedMembers` (BSTR)
- **ContactSolid**: `General` (Solid), `SurfaceANo` (c_int), `SurfaceBNo` (c_int), `Perpendicular` (PerpendicularContactType), `Parallel` (ParallelContactType), `SpringStiffness` (c_double), `CoulombFrictionFactor` (c_double), `ShearStress` (c_double)
- **CoordinateSystem**: `Origin` (Point3D), `AxisX` (Point3D), `AxisY` (Point3D), `AxisZ` (Point3D), `IsVertical` (VARIANT_BOOL), `IsAxisZUp` (VARIANT_BOOL), `Rotation` (c_double), `Epsilon` (c_double)
- **CrossSection**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `Description` (BSTR), `TextID` (BSTR), `UserDefined` (VARIANT_BOOL), `MaterialNo` (c_int), `Rotation` (c_double), `Angle` (c_double), `TorsionMoment` (c_double), `BendingMomentY` (c_double), `BendingMomentZ` (c_double), `AxialArea` (c_double), `ShearAreaY` (c_double), `ShearAreaZ` (c_double), `TemperatureLoadWidth` (c_double), `TemperatureLoadDepth` (c_double)
- **Dimension**: `No` (c_int), `ID` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `Type` (DimensionObjectType), `ObjectList` (BSTR), `Values` (c_double[]), `Symbol` (BSTR)
- **DimensionOptions**: `ShowReferenceLabel` (VARIANT_BOOL), `ShowUnit` (VARIANT_BOOL), `ShowSymbol` (VARIANT_BOOL), `HideValue` (VARIANT_BOOL)
- **ErrorInfo**: `ModuleName` (BSTR), `Load` (Loading), `ErrorNo` (c_int), `Type` (ErrorType), `Description` (BSTR)
- **FeMesh1DElement**: `No` (c_int), `MemberNo` (c_int), `NodeNumbers` (c_int * 2)
- **FeMesh2DElement**: `No` (c_int), `SurfaceNo` (c_int), `NodeNumbers` (c_int * 4)
- **FeMesh3DElement**: `No` (c_int), `SolidNo` (c_int), `NodeNumbers` (c_int * 8)
- **FeMeshGeneralSettings**: `ElementLength` (c_double), `MaxDistanceNodeToLine` (c_double), `MaxNodes` (c_int)
- **FeMeshMembersSettings**: `DivideConcreteMembers` (VARIANT_BOOL), `MinConcreteMemberDivisions` (c_int), `DivideStraightMembers` (VARIANT_BOOL), `ElementLength` (c_double), `MinStraightMemberDivisions` (c_int)
- **FeMeshNode**: `No` (c_int), `X` (c_double), `Y` (c_double), `Z` (c_double)
- **FeMeshRefinement**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `ObjectList` (BSTR), `Type` (FeMeshRefinementType), `Number` (c_int), `Layers` (c_int), `Length` (c_double), `TargetLengthInner` (c_double), `TargetLengthOuter` (c_double)
- **FeMeshSolidsSettings**: `RefinementCloseNodes` (VARIANT_BOOL), `MaxElements` (c_int)
- **FeMeshSurfacesSettings**: `MaxRectangleDiagonals` (c_double), `MaxInclination` (c_double), `RefinementAlongLines` (VARIANT_BOOL), `RefinementRelationship` (c_double), `UnutilizedObjectsIntoSurfaces` (VARIANT_BOOL), `Shape` (FiniteElementsShape), `SameSquares` (VARIANT_BOOL), `MappedMeshPreferred` (VARIANT_BOOL)
- **FormulaParameter**: `No` (c_int), `Comment` (BSTR), `IsValid` (VARIANT_BOOL), `Name` (BSTR), `UnitType` (UnitType), `Unit` (BSTR), `ValueType` (DataType), `Value` (BSTR), `Formula` (BSTR), `RangeOfValues` (BSTR)
- **FreeCircularLoad**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `SurfaceList` (BSTR), `ProjectionPlane` (PlaneType), `Direction` (LoadDirectionType), `Distribution` (LoadDistributionType), `Magnitude1` (c_double), `Magnitude2` (c_double), `Position` (Point3D), `Radius` (c_double)
- **FreeConcentratedLoad**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `SurfaceList` (BSTR), `ProjectionPlane` (PlaneType), `Direction` (LoadDirectionType), `Type` (LoadType), `Magnitude` (c_double), `Position` (Point3D)
- **FreeLineLoad**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `SurfaceList` (BSTR), `ProjectionPlane` (PlaneType), `Direction` (LoadDirectionType), `Distribution` (LoadDistributionType), `Magnitude1` (c_double), `Magnitude2` (c_double), `Position1` (Point3D), `Position2` (Point3D)
- **FreePolygonLoad**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `SurfaceList` (BSTR), `ProjectionPlane` (PlaneType), `Direction` (LoadDirectionType), `Distribution` (LoadDistributionType), `CornerPointList` (BSTR), `Position` (c_double), `Point1No` (c_int), `Point2No` (c_int), `Point3No` (c_int), `Magnitude1` (c_double), `Magnitude2` (c_double), `Magnitude3` (c_double)
- **FreeRectangularLoad**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `SurfaceList` (BSTR), `ProjectionPlane` (PlaneType), `Direction` (LoadDirectionType), `Distribution` (LoadDistributionType), `Magnitude1` (c_double), `Magnitude2` (c_double), `Position1` (Point3D), `Position2` (Point3D)
- **Friction**: `Coefficient1` (c_double), `Coefficient2` (c_double)
- **GasSolid**: `General` (Solid), `Pressure` (c_double), `Temperature` (c_double)
- **Grid**: `ShowGrid` (VARIANT_BOOL), `ShowSnap` (VARIANT_BOOL), `SnapDistance` (c_int), `IsPolar` (VARIANT_BOOL), `DynamicGrid` (VARIANT_BOOL), `PointsIn1Positive` (c_int), `PointsIn1Negative` (c_int), `PointsIn2Positive` (c_int), `PointsIn2Negative` (c_int), `PointSpacing1` (c_double), `PointSpacing2` (c_double), `Rotation` (c_double), `LineSpacing1` (c_int), `LineSpacing2` (c_int)
- **Guideline**: `No` (c_int), `ID` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `WorkPlane` (PlaneType), `WorkPlaneOrigin` (Point3D), `Type` (GuidelineType), `Point1` (Point3D), `Point2` (Point3D), `Angle` (c_double), `Radius` (c_double), `Description` (BSTR)
- **HeightDimension**: `No` (c_int), `ID` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `NodeNo` (c_int), `Offset` (c_double), `Rotation` (c_double), `ReferenceHeight` (c_double), `Symbol` (BSTR)
- **Imperfection**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `ReferenceTo` (MemberLoadReferenceType), `ObjectList` (BSTR), `Direction` (LoadDirectionType), `Reference` (ReferenceType), `Inclination` (c_double), `Precamber` (c_double), `PrecamberActivity` (PrecamberActivityCriterionType), `PrecamberCriterion` (c_double)
- **ImposedLineDisplacement**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `LineList` (BSTR), `Start` (Point3D), `End` (Point3D)
- **ImposedNodalDeformation**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `NodeList` (BSTR), `Displacement` (Point3D), `Rotation` (Point3D)
- **IncrementallyIncreasingLoading**: `Activate` (VARIANT_BOOL), `InitialLoadFactor` (c_double), `LoadFactorIncrement` (c_double), `LastLoadIncrementRefinement` (c_int), `StoppingCondition` (StoppingConditionType), `NodeNo` (c_int), `Value` (c_double), `IntialLoad` (Loading)
- **InternalPressure**: `DisplacementsDueToPressure` (VARIANT_BOOL)
- **IntersectionOfSurfaces**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `Surface1No` (c_int), `Surface2No` (c_int), `LineList` (BSTR)
- **IsolineArc**: `Center` (Point3D), `Extrusion` (Point3D), `Radius` (c_double), `StartAngle` (c_double), `EndAngle` (c_double), `LayerName` (BSTR)
- **IsolineCircle**: `Center` (Point3D), `Extrusion` (Point3D), `Radius` (c_double), `LayerName` (BSTR)
- **IsolineLayer**: `Visible` (VARIANT_BOOL), `Name` (BSTR), `Flag` (c_int), `Color` (c_int), `Thickness` (c_int)
- **IsolineLine**: `Start` (Point3D), `End` (Point3D), `LayerName` (BSTR)
- **IsolinePoint**: `Label` (c_int), `Indexes` (c_int * 4), `Position` (Point3D), `LayerName` (BSTR)
- **IsolineStyle**: `Name` (BSTR), `StandartFlags` (c_int), `Height` (c_double), `WidthFactor` (c_double), `Angle` (c_double), `TextFlags` (c_int), `LastHeight` (c_double), `FontFileName` (BSTR)
- **IsolineText**: `Position` (Point3D), `Height` (c_double), `Text` (BSTR), `Rotation` (c_double), `StyleName` (BSTR), `LayerName` (BSTR), `Extrusion` (Point3D)
- **Line**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `IsGenerated` (VARIANT_BOOL), `Type` (LineType), `NodeCount` (c_int), `NodeList` (BSTR), `Length` (c_double), `Rotation` (Rotation), `ControlPoints` (Point3D[])
- **LineHinge**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `LineNo` (c_int), `SurfaceNo` (c_int), `Side` (HingeSideType), `TranslationalConstantX` (c_double), `TranslationalConstantY` (c_double), `TranslationalConstantZ` (c_double), `RotationalConstantX` (c_double), `RotationalConstantY` (c_double), `RotationalConstantZ` (c_double)
- **LineLoad**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `ReferenceTo` (LineLoadReferenceType), `LineList` (BSTR), `Type` (LoadType), `Distribution` (LoadDistributionType), `Direction` (LoadDirectionType), `Magnitude1` (c_double), `Magnitude2` (c_double), `Magnitude3` (c_double), `DistanceA` (c_double), `DistanceB` (c_double), `LoadArray` (c_double[]), `RelativeDistances` (VARIANT_BOOL), `OverTotalLength` (VARIANT_BOOL)
- **LineOnSurface**: `General` (Line), `SurfaceNo` (c_int), `StartPosition1` (c_double), `StartPosition2` (c_double), `EndPosition1` (c_double), `EndPosition2` (c_double)
- **LineRelease**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `LineNo` (c_int), `TypeNo` (c_int), `AxisSystem` (LineReleaseAxisSystem), `AxisSystemFromObjectNo` (c_int), `HelpNodePlane` (PlaneType), `Rotation` (c_double), `ReleasedMembers` (BSTR), `ReleasedSurfaces` (BSTR), `ReleasedSolids` (BSTR), `Location` (ReleaseLocation), `GeneratedLineNo` (c_int), `DefinitionNodes` (BSTR)
- **LineReleaseType**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `TranslationalConstantX` (c_double), `TranslationalConstantY` (c_double), `TranslationalConstantZ` (c_double), `RotationalConstantX` (c_double), `TranslationalNonlinearityX` (NonlinearityType), `TranslationalNonlinearityY` (NonlinearityType), `TranslationalNonlinearityZ` (NonlinearityType), `RotationalNonlinearityX` (NonlinearityType)
- **LineSupport**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `LineList` (BSTR), `ReferenceSystem` (ReferenceSystemType), `Rotation` (c_double), `IsWall` (VARIANT_BOOL), `Wall` (Wall), `SupportConstantX` (c_double), `SupportConstantY` (c_double), `SupportConstantZ` (c_double), `RestraintConstantX` (c_double), `RestraintConstantY` (c_double), `RestraintConstantZ` (c_double), `SupportNonlinearityX` (NonlinearityType), `SupportNonlinearityY` (NonlinearityType), `SupportNonlinearityZ` (NonlinearityType)
- **LineSupport2**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `LineList` (BSTR), `ReferenceSystem` (ReferenceSystemType), `Rotation` (c_double), `IsWall` (VARIANT_BOOL), `Wall` (Wall), `SupportConstantX` (c_double), `SupportConstantY` (c_double), `SupportConstantZ` (c_double), `RestraintConstantX` (c_double), `RestraintConstantY` (c_double), `RestraintConstantZ` (c_double), `SupportNonlinearityX` (NonlinearityType), `SupportNonlinearityY` (NonlinearityType), `SupportNonlinearityZ` (NonlinearityType), `RestraintNonlinearityX` (NonlinearityType), `RestraintNonlinearityY` (NonlinearityType), `RestraintNonlinearityZ` (NonlinearityType)
- **LineSupportForces**: `LineNo` (c_int), `NodeNo` (c_int), `Flag` (ResultsFlag), `Type` (ResultsValueType), `Location` (c_double), `Forces` (Point3D), `Moments` (Point3D)
- **LinearDimension**: `No` (c_int), `ID` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `NodeList` (BSTR), `Reference` (DimensionReferenceType), `CoordinateSystemNo` (c_int), `Plane` (DimensionPlaneType), `LocalOffset` (VARIANT_BOOL), `Offset` (Point3D), `Lengths` (c_double[]), `Symbol` (BSTR)
- **LoadAxis**: `Definition` (LoadAxisDefinitionType), `ParallelAxis` (LoadAxisType), `Point1` (Point3D), `Point2` (Point3D)
- **LoadCase**: `Loading` (Loading), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `Description` (BSTR), `ToSolve` (VARIANT_BOOL), `ActionCategory` (ActionCategoryType), `UserDefinedAction` (BSTR), `SelfWeight` (VARIANT_BOOL), `SelfWeightFactor` (Point3D)
- **LoadCombination**: `Loading` (Loading), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `DesignSituation` (DesignSituationType), `Description` (BSTR), `ToSolve` (VARIANT_BOOL), `Definition` (BSTR)
- **Loading**: `Type` (LoadingType), `No` (c_int)
- **ManipulationCopy**: `Copies` (c_int), `Vector` (Point3D), `NodesIncrement` (c_int), `MembersIncrement` (c_int), `LinesIncrement` (c_int), `SurfacesIncrement` (c_int), `SolidsIncrement` (c_int)
- **ManipulationMirror**: `CreateCopy` (VARIANT_BOOL), `MirroringPlane` (PlaneType), `Point1` (Point3D), `Point2` (Point3D), `Point3` (Point3D), `NodesIncrement` (c_int), `MembersIncrement` (c_int), `LinesIncrement` (c_int), `SurfacesIncrement` (c_int), `SolidsIncrement` (c_int)
- **ManipulationProject**: `CreateCopy` (VARIANT_BOOL), `ProjectionDirection` (AxisType), `Point1` (Point3D), `Point2` (Point3D), `Point3` (Point3D), `NodesIncrement` (c_int), `MembersIncrement` (c_int), `LinesIncrement` (c_int), `SurfacesIncrement` (c_int), `SolidsIncrement` (c_int)
- **ManipulationRotate**: `Copies` (c_int), `Angle` (c_double), `AxisDirection` (AxisType), `Point1` (Point3D), `Point2` (Point3D), `NodesIncrement` (c_int), `MembersIncrement` (c_int), `LinesIncrement` (c_int), `SurfacesIncrement` (c_int), `SolidsIncrement` (c_int)
- **ManipulationScale**: `Copies` (c_int), `Factor` (c_double), `Direction` (ScalingDirectionType), `AxisDirection` (AxisType), `Point1` (Point3D), `Point2` (Point3D), `NodesIncrement` (c_int), `MembersIncrement` (c_int), `LinesIncrement` (c_int), `SurfacesIncrement` (c_int), `SolidsIncrement` (c_int)
- **ManipulationShear**: `SlopeFactor` (c_double), `SlopeAngle` (c_double), `AboutAxis` (AxisType), `InDirection` (AxisType), `Point1` (Point3D), `Point2` (Point3D), `Point3` (Point3D)
- **Material**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `Description` (BSTR), `TextID` (BSTR), `UserDefined` (VARIANT_BOOL), `ElasticityModulus` (c_double), `ShearModulus` (c_double), `PoissonRatio` (c_double), `SpecificWeight` (c_double), `ThermalExpansion` (c_double), `PartialSafetyFactor` (c_double), `ModelType` (MaterialModelType)
- **MaterialIsotropicMasonry2DModel**: `No` (c_int), `LimitTensionStressesX` (c_double), `LimitTensionStressesY` (c_double), `HardeningFactor` (c_double), `LinearElasticOnly` (VARIANT_BOOL)
- **MaterialIsotropicModel**: `No` (c_int), `Definition` (MaterialModelDefinitionType), `YieldStrengthInTension` (c_double), `YieldStrengthInCompression` (c_double), `StrainHardeningModulus` (c_double), `LinearElasticOnly` (VARIANT_BOOL), `StrainHypothesis` (MaterialStrainHypothesisType)
- **MaterialIsotropicThermalElasticModel**: `No` (c_int), `TemperatureDiagram` (MaterialTemperatureDiagramItem[]), `ReferenceTemperature` (c_double), `Comment` (BSTR)
- **MaterialOrthotropicElasticModel**: `No` (c_int), `ElasticityModulusX` (c_double), `ElasticityModulusY` (c_double), `ElasticityModulusZ` (c_double), `ShearModulusYZ` (c_double), `ShearModulusXZ` (c_double), `ShearModulusXY` (c_double), `PoissonRatioYZ` (c_double), `PoissonRatioXZ` (c_double), `PoissonRatioXY` (c_double)
- **MaterialOrthotropicPlasticModel**: `No` (c_int), `ElasticityModulusX` (c_double), `ElasticityModulusY` (c_double), `ElasticityModulusZ` (c_double), `ShearModulusYZ` (c_double), `ShearModulusXZ` (c_double), `ShearModulusXY` (c_double), `PoissonRatioYZ` (c_double), `PoissonRatioXZ` (c_double), `PoissonRatioXY` (c_double), `HardeningModulus` (c_double), `UltimateTensileStrengthX` (c_double), `UltimateTensileStrengthY` (c_double), `UltimateTensileStrengthZ` (c_double), `UltimateCompressiveStrengthX` (c_double), `UltimateCompressiveStrengthY` (c_double), `UltimateCompressiveStrengthZ` (c_double), `UltimateShearStrengthYZ` (c_double), `UltimateShearStrengthXZ` (c_double), `UltimateShearStrengthXY` (c_double), `LinearElasticOnly` (VARIANT_BOOL)
- **MaterialTemperatureDiagramItem**: `Temperature` (c_double), `ElasticityModulus` (c_double), `ShearModulus` (c_double), `PoissonRatio` (c_double), `ThermalExpansion` (c_double)
- **MaximumResults**: `Displacement` (Point3D), `VectorialDisplacement` (c_double), `Rotation` (Point3D)
- **Member**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `IsGenerated` (VARIANT_BOOL), `LineNo` (c_int), `Type` (MemberType), `Rotation` (Rotation), `StartCrossSectionNo` (c_int), `EndCrossSectionNo` (c_int), `TaperShape` (TaperShapeType), `StartHingeNo` (c_int), `EndHingeNo` (c_int), `EccentricityNo` (c_int), `DivisionNo` (c_int), `FoundationNo` (c_int), `NonlinearityNo` (c_int), `RibNo` (c_int), `Length` (c_double), `Weight` (c_double)
- **MemberDeformations**: `MemberNo` (c_int), `Flag` (ResultsFlag), `Type` (ResultsValueType), `Location` (c_double), `TotalDisplacement` (c_double), `Displacements` (Point3D), `Rotations` (Point3D)
- **MemberDivision**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `IntermediatePoints` (c_int), `Distances` (c_double[])
- **MemberEccentricity**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `IsGenerated` (VARIANT_BOOL), `ReferenceSystem` (ReferenceSystemType), `Start` (Point3D), `End` (Point3D), `HorizontalAlignment` (HorizontalAlignmentType), `VerticalAlignment` (VerticalAlignmentType), `TransverseOffset` (VARIANT_BOOL), `ReferenceObjectType` (ModelObjectType), `ReferenceObjectNo` (c_int), `HorizontalAxisOffset` (HorizontalAlignmentType), `VerticalAxisOffset` (VerticalAlignmentType), `StartAdjoiningMembersOffset` (VARIANT_BOOL), `EndAdjoiningMembersOffset` (VARIANT_BOOL), `HingeAtStartNode` (VARIANT_BOOL), `HingeAtEndNode` (VARIANT_BOOL)
- **MemberEffectiveLengths**: `No` (c_int), `Enabled` (VARIANT_BOOL), `FactorY` (c_double), `FactorZ` (c_double), `FactorU` (c_double), `FactorV` (c_double), `EffectiveLengthY` (c_double), `EffectiveLengthZ` (c_double), `EffectiveLengthU` (c_double), `EffectiveLengthV` (c_double), `CriticalBucklingLoad` (c_double), `CheckBucklingLoad` (VARIANT_BOOL)
- **MemberElasticFoundation**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `MemberList` (BSTR), `TranslationX` (c_double), `TranslationY` (c_double), `TranslationZ` (c_double), `ShearX` (c_double), `ShearY` (c_double), `ShearZ` (c_double), `Rotation` (c_double), `Ineffective` (IneffectiveFoundationType)
- **MemberForces**: `MemberNo` (c_int), `CrossSectionNo` (c_int), `SetNo` (c_int), `Flag` (ResultsFlag), `Type` (ResultsValueType), `Location` (c_double), `Forces` (Point3D), `Moments` (Point3D), `CorrespondingLoading` (BSTR)
- **MemberHinge**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `ReferenceSystem` (ReferenceSystemType), `UserDefinedReferenceSystem` (UserDefinedAxisSystem), `TranslationalConstantX` (c_double), `TranslationalConstantY` (c_double), `TranslationalConstantZ` (c_double), `RotationalConstantX` (c_double), `RotationalConstantY` (c_double), `RotationalConstantZ` (c_double), `TranslationalNonlinearityX` (NonlinearityType), `TranslationalNonlinearityY` (NonlinearityType), `TranslationalNonlinearityZ` (NonlinearityType), `RotationalNonlinearityX` (NonlinearityType), `RotationalNonlinearityY` (NonlinearityType), `RotationalNonlinearityZ` (NonlinearityType), `TranslationalSpecialX` (VARIANT_BOOL), `TranslationalSpecialY` (VARIANT_BOOL), `TranslationalSpecialZ` (VARIANT_BOOL), `RotationalSpecialX` (VARIANT_BOOL), `RotationalSpecialY` (VARIANT_BOOL), `RotationalSpecialZ` (VARIANT_BOOL)
- **MemberLoad**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `ReferenceTo` (MemberLoadReferenceType), `ObjectList` (BSTR), `Type` (LoadType), `Distribution` (LoadDistributionType), `Direction` (LoadDirectionType), `Magnitude1` (c_double), `Magnitude2` (c_double), `Magnitude3` (c_double), `Magnitude4` (c_double), `Magnitude5` (c_double), `Magnitude6` (c_double), `DistanceA` (c_double), `DistanceB` (c_double), `RotaryMotionAxis` (LoadAxis), `LoadArray` (c_double[]), `RelativeDistances` (VARIANT_BOOL), `OverTotalLength` (VARIANT_BOOL)
- **MemberNonlinearity**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `MemberList` (BSTR), `Type` (MemberNonlinearityType), `Parameters` (c_double[])
- **MemberStiffnessFactors**: `No` (c_int), `Enabled` (VARIANT_BOOL), `TorsionalStiffness` (c_double), `FlexuralStiffnessY` (c_double), `FlexuralStiffnessZ` (c_double), `AxialStiffness` (c_double), `ShearStiffnessY` (c_double), `ShearStiffnessZ` (c_double)
- **NodalDeformations**: `NodeNo` (c_int), `Type` (ResultsValueType), `TotalDisplacement` (c_double), `Displacements` (Point3D), `Rotations` (Point3D)
- **NodalLoad**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `NodeList` (BSTR), `Definition` (LoadDefinitionType), `Component` (NodalLoadComponent), `Direction` (NodalLoadDirection)
- **NodalLoadComponent**: `CoordinateSystemNo` (c_int), `Force` (Point3D), `Moment` (Point3D)
- **NodalLoadDirection**: `Type` (NodalLoadDirectionType), `RotationSequence` (RotationSequence), `RotationAngles` (Point3D), `ObjectNo` (c_int), `Object2No` (c_int), `Force` (c_double), `Moment` (c_double)
- **NodalRelease**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `NodeNo` (c_int), `MemberHingeNo` (c_int), `AxisSystem` (NodalReleaseAxisSystem), `AxisSystemFromObjectNo` (c_int), `ReleasedMembers` (BSTR), `ReleasedSurfaces` (BSTR), `ReleasedSolids` (BSTR), `Location` (ReleaseLocation), `GeneratedNodeNo` (c_int)
- **NodalSupport**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `NodeList` (BSTR), `ReferenceSystem` (ReferenceSystemType), `UserDefinedReferenceSystem` (UserDefinedAxisSystem), `IsColumn` (VARIANT_BOOL), `Column` (Column), `SupportConstantX` (c_double), `SupportConstantY` (c_double), `SupportConstantZ` (c_double), `RestraintConstantX` (c_double), `RestraintConstantY` (c_double), `RestraintConstantZ` (c_double), `SupportNonlinearityX` (NonlinearityType), `SupportNonlinearityY` (NonlinearityType), `SupportNonlinearityZ` (NonlinearityType), `RestraintNonlinearityX` (NonlinearityType), `RestraintNonlinearityY` (NonlinearityType), `RestraintNonlinearityZ` (NonlinearityType)
- **NodalSupportForces**: `NodeNo` (c_int), `Type` (ResultsValueType), `Forces` (Point3D), `Moments` (Point3D), `CorrespondingLoading` (BSTR)
- **Node**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `IsGenerated` (VARIANT_BOOL), `RefObjectNo` (c_int), `X` (c_double), `Y` (c_double), `Z` (c_double), `CS` (CoordinateSystemType), `Type` (NodeType), `Delta1` (c_double), `Delta2` (c_double)
- **NonlinearityDiagram**: `ForceType` (StiffnessDiagramForceType), `PositiveZoneType` (DiagramAfterLastStepType), `PositiveZone` (c_double[]), `Symmetric` (VARIANT_BOOL), `NegativeZoneType` (DiagramAfterLastStepType), `NegativeZone` (c_double[]), `Comment` (BSTR)
- **NurbSpline**: `General` (Line), `Order` (c_int), `Weights` (c_double[]), `Knots` (c_double[])
- **NurbsSurface**: `General` (Surface), `OrderX` (c_int), `OrderY` (c_int), `Nodes` (c_int[]), `Weights` (c_double[]), `KnotsX` (c_double[]), `KnotsY` (c_double[])
- **Opening**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `IsGenerated` (VARIANT_BOOL), `Area` (c_double), `InSurfaceNo` (c_int), `BoundaryLineCount` (c_int), `BoundaryLineList` (BSTR)
- **Parabola**: `General` (Line), `Angle` (c_double), `ParameterP` (c_double), `Focus` (Point3D)
- **PartialActivity**: `PositiveZone` (PartialActivityType), `PositiveLimit` (c_double), `PositiveSlippage` (c_double), `NegativeZone` (PartialActivityType), `NegativeLimit` (c_double), `NegativeSlippage` (c_double)
- **PipeSurface**: `General` (Surface), `CenterLineNo` (c_int), `Radius` (c_double), `Optimize` (VARIANT_BOOL), `NeighboringSurfaceNo` (c_int), `GeneratedLineList` (BSTR)
- **PlasticHinge**: `Type` (PlasticHingeType), `Antimetric` (VARIANT_BOOL), `UserDefinedType` (VARIANT_BOOL), `AutomaticType` (VARIANT_BOOL), `DiagramParameters` (c_double[]), `NegativeYieldForceOrMoment` (c_double), `PositiveYieldForceOrMoment` (c_double), `NegativeYieldDeformationOrRotation` (c_double), `PositiveYieldDeformationOrRotation` (c_double), `AcceptanceCriteriaType` (PlasticHingeAcceptanceCriteriaType), `NegativeImmediateOccupancy` (c_double), `PositiveImmediateOccupancy` (c_double), `NegativeLifeSafety` (c_double), `PositiveLifeSafety` (c_double), `NegativeCollapsePrevention` (c_double), `PositiveCollapsePrevention` (c_double)
- **Point3D**: `X` (c_double), `Y` (c_double), `Z` (c_double)
- **PrecisionAndTolerance**: `ChangeStandardSettings` (VARIANT_BOOL), `ConvergencePrecision` (c_double), `InstabilityDetection` (c_double), `DynamicRelaxationTimeStep` (c_double), `IterativeCalculationRobustness` (c_double), `MinimumInitialStrain` (c_double), `AlwaysUseMinimumStrain` (VARIANT_BOOL)
- **Protocol**: `No` (c_int), `Description` (BSTR)
- **ProtocolCompany**: `Address1` (BSTR), `Address1Alignment` (HorizontalAlignmentType), `Address2` (BSTR), `Address2Alignment` (HorizontalAlignmentType), `Address3` (BSTR), `Address3Alignment` (HorizontalAlignmentType), `LogoPath` (BSTR)
- **ProtocolDate**: `Type` (ProtocolDateType), `Date` (c_double)
- **ProtocolHeaderOptions**: `Header` (VARIANT_BOOL), `InfoRowBellowHeader` (VARIANT_BOOL), `Footer` (VARIANT_BOOL), `BlackCircles` (VARIANT_BOOL), `Date` (VARIANT_BOOL), `CompanyLogo` (VARIANT_BOOL), `PageNumber` (VARIANT_BOOL), `SheetNumber` (VARIANT_BOOL)
- **ProtocolNumbering**: `FirstPageNo` (c_int), `FirstSheetNo` (c_int)
- **QuadraticCombination**: `Loading` (Loading), `Enable` (VARIANT_BOOL), `PreserveSigns` (VARIANT_BOOL), `Type` (QuadraticCombinationType)
- **RadialDimension**: `No` (c_int), `ID` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `LineNo` (c_int), `Type` (RadialDimensionType), `View` (RadialDimensionViewType), `ViewParameter` (c_double), `Offset` (c_double), `Length` (c_double), `Symbol` (BSTR), `UseTargetPoint` (VARIANT_BOOL), `TargetPoint` (Point3D)
- **ReactivationOfFailingMembers**: `CheckDeformation` (VARIANT_BOOL), `MaxReactivations` (c_int), `ExceptionalHandling` (ExceptionalHandlingType), `StiffnessReductionFactor` (c_double)
- **ResultBeam**: `No` (c_int), `Integrate` (IntegrateStressesAndForcesType), `Parameters` (c_double[]), `IncludeSurfaces` (BSTR), `IncludeSolids` (BSTR), `IncludeMembers` (BSTR), `ExceptSurfaces` (BSTR), `ExceptSolids` (BSTR), `ExceptMembers` (BSTR)
- **ResultCombination**: `Loading` (Loading), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `DesignSituation` (DesignSituationType), `Description` (BSTR), `ToSolve` (VARIANT_BOOL), `Definition` (BSTR)
- **ResultantForce**: `SectionNo` (c_int), `CenterOfGravity` (Point3D), `Forces` (Point3D), `Moments` (Point3D)
- **Rib**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `Position` (RibPositionType), `SurfaceNoSide1` (c_int), `WidthSide1` (c_double), `SurfaceNoSide2` (c_int), `WidthSide2` (c_double), `AlignLocalZAxis` (VARIANT_BOOL)
- **RibCrossSection**: `RibNo` (c_int), `IsValid` (VARIANT_BOOL), `Description` (BSTR), `Depth` (c_double), `WebThickness` (c_double), `UpperLeftFlangeWidth` (c_double), `UpperLeftFlangeThickness` (c_double), `UpperLeftChamferWidth` (c_double), `UpperLeftChamferHeight` (c_double), `LowerLeftFlangeWidth` (c_double), `LowerLeftFlangeThickness` (c_double), `LowerLeftChamferWidth` (c_double), `LowerLeftChamferHeight` (c_double), `UpperRightFlangeWidth` (c_double), `UpperRightFlangeThickness` (c_double), `UpperRightChamferWidth` (c_double), `UpperRightChamferHeight` (c_double), `LowerRightFlangeWidth` (c_double), `LowerRightFlangeThickness` (c_double), `LowerRightChamferWidth` (c_double), `LowerRightChamferHeight` (c_double), `Eccentricity` (Point3D)
- **RotatedSurface**: `General` (Surface), `BoundaryLineNo` (c_int), `Rotation` (c_double), `Start` (Point3D), `End` (Point3D), `GeneratedLineList` (BSTR)
- **Rotation**: `Type` (RotationType), `Angle` (c_double), `HelpNodeNo` (c_int), `Plane` (PlaneType)
- **Scaffolding**: `Slip` (c_double), `Stiffness` (c_double), `DefinitionType` (ScaffoldingDefinitionType), `SlipEccentricity` (c_double), `SlipEccentricityFactor` (c_double), `MaximumEccentricity` (c_double), `MaximumEccentricityFactor` (c_double), `MemberNo` (c_int), `Diameter` (c_double)
- **Section**: `No` (c_int), `ID` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `IsGenerated` (VARIANT_BOOL), `Name` (BSTR), `Type` (SectionType), `EdgePointA` (Point3D), `EdgePointB` (Point3D), `Vector` (Point3D), `Plane` (SectionPlaneType), `LineList` (BSTR), `ObjectList` (BSTR), `ShowValuesInIsolines` (VARIANT_BOOL)
- **SectionResult**: `SectionNo` (c_int), `Location` (c_double), `LocationPoint` (Point3D), `Value` (c_double)
- **SetOfMembers**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `Description` (BSTR), `Type` (SetOfMembersType), `MemberList` (BSTR), `Length` (c_double), `Weight` (c_double)
- **SlopeDimension**: `No` (c_int), `ID` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `LineNo` (c_int), `Plane` (PlaneType), `Direction` (OrientationType), `Offset` (c_double), `Angle` (c_double), `Symbol` (BSTR)
- **Solid**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `IsGenerated` (VARIANT_BOOL), `Type` (SolidType), `SurfaceList` (BSTR), `MaterialNo` (c_int), `Compound` (VARIANT_BOOL), `Volume` (c_double), `Weight` (c_double)
- **SolidAxes**: `No` (c_int), `Direction` (SolidAxesDirection), `SurfaceNo` (c_int), `LineList` (BSTR), `Point` (Point3D), `UserCSNo` (c_int)
- **SolidCriteria**: `SolidNo` (c_int), `SurfaceNo` (c_int), `Type` (ResultsValueType), `LocationNo` (c_int), `Coordinates` (Point3D), `NonlinearityRate` (c_double), `DesignRatio` (c_double), `EquivalentPlasticStrain` (c_double), `EquivalentCrackStrain` (c_double), `StiffnessReduction` (c_double)
- **SolidDeformations**: `SolidNo` (c_int), `SurfaceNo` (c_int), `Type` (ResultsValueType), `LocationNo` (c_int), `Coordinates` (Point3D), `TotalDisplacement` (c_double), `Displacements` (Point3D), `Rotations` (Point3D)
- **SolidGasPressure**: `SolidNo` (c_int), `SurfaceNo` (c_int), `Type` (ResultsValueType), `LocationNo` (c_int), `Coordinates` (Point3D), `Pressure` (c_double)
- **SolidLoad**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `SolidList` (BSTR), `Type` (LoadType), `Distribution` (LoadDistributionType), `Direction` (LoadDirectionType), `Node1No` (c_int), `Magnitude1` (c_double), `Node2No` (c_int), `Magnitude2` (c_double), `RotaryMotionAxis` (LoadAxis), `Buoyancy` (Buoyancy)
- **SolidPlasticStrains**: `SolidNo` (c_int), `SurfaceNo` (c_int), `Type` (ResultsValueType), `LocationNo` (c_int), `Coordinates` (Point3D), `EpsilonPX` (c_double), `EpsilonPY` (c_double), `EpsilonPZ` (c_double), `GammaPYZ` (c_double), `GammaPXZ` (c_double), `GammaPXY` (c_double)
- **SolidStrains**: `SolidNo` (c_int), `SurfaceNo` (c_int), `Type` (ResultsValueType), `LocationNo` (c_int), `Coordinates` (Point3D), `EpsilonX` (c_double), `EpsilonY` (c_double), `EpsilonZ` (c_double), `GammaYZ` (c_double), `GammaXZ` (c_double), `GammaXY` (c_double), `Epsilon1` (c_double), `Epsilon2` (c_double), `Epsilon3` (c_double), `EpsilonMises` (c_double), `EpsilonTresca` (c_double), `EpsilonRankine` (c_double), `EpsilonBach` (c_double)
- **SolidStresses**: `SolidNo` (c_int), `SurfaceNo` (c_int), `Type` (ResultsValueType), `LocationNo` (c_int), `Coordinates` (Point3D), `SigmaX` (c_double), `SigmaY` (c_double), `SigmaZ` (c_double), `TauYZ` (c_double), `TauXZ` (c_double), `TauXY` (c_double), `TauMax` (c_double), `Sigma1` (c_double), `Sigma2` (c_double), `Sigma3` (c_double), `SigmaEqvMises` (c_double), `SigmaEqvTresca` (c_double), `SigmaEqvRankine` (c_double), `SigmaEqvBach` (c_double)
- **SpringBeam**: `No` (c_int), `Definition` (SpringDefinitionType), `Parameters` (SpringBeamParameters), `Diagram` (NonlinearityDiagram), `SelfWeight` (SelfWeightType), `SelfWeightParameters` (c_double[])
- **SpringBeamParameters**: `AxialStiffness` (c_double), `PositiveSlippage` (c_double), `NegativeSlippage` (c_double), `Limits` (SpringLimitsType), `MinLimit` (c_double), `MaxLimit` (c_double)
- **StiffnessBeam**: `No` (c_int), `TorsionalStiffness` (c_double), `FlexuralStiffnessV` (c_double), `FlexuralStiffnessZ` (c_double), `AxialStiffness` (c_double), `ShearStiffnessV` (c_double), `ShearStiffnessZ` (c_double), `SpecificWeight` (c_double), `CrossSectionArea` (c_double), `ThermalExpansion` (c_double), `Width` (c_double), `Height` (c_double)
- **StiffnessGeometricProperties**: `Diameter` (c_double), `Height` (c_double), `HeightX` (c_double), `HeightY` (c_double), `Spacing` (c_double), `SpacingX` (c_double), `SpacingY` (c_double), `Thickness` (c_double), `ThicknessX` (c_double), `ThicknessY` (c_double), `Width` (c_double), `WidthX` (c_double), `WidthY` (c_double), `TopFlangeWidth` (c_double), `BottomFlangeWidth` (c_double)
- **StiffnessMatrix**: `No` (c_int), `D11` (c_double), `D12` (c_double), `D22` (c_double), `D13` (c_double), `D23` (c_double), `D33` (c_double), `D44` (c_double), `D45` (c_double), `D55` (c_double), `D66` (c_double), `D67` (c_double), `D77` (c_double), `D68` (c_double), `D78` (c_double), `D88` (c_double), `D16` (c_double), `D17` (c_double), `D27` (c_double), `D18` (c_double), `D28` (c_double), `D38` (c_double)
- **StiffnessMultiplicationFactors**: `K` (c_double), `Kb` (c_double), `K33` (c_double), `Ks` (c_double), `K44` (c_double), `K55` (c_double), `Km` (c_double), `Ke` (c_double)
- **StiffnessMultiplicationFactors2**: `K` (c_double), `Kb` (c_double), `K33` (c_double), `Ks` (c_double), `K44` (c_double), `K55` (c_double), `Km` (c_double), `K88` (c_double), `Ke` (c_double)
- **SummaryResults**: `Loads` (Point3D), `SupportForces` (Point3D)
- **SummarySupportForces**: `Forces` (Point3D), `Loads` (Point3D)
- **SuperCombination**: `Loading` (Loading), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `DesignSituation` (DesignSituationType), `Description` (BSTR), `ToSolve` (VARIANT_BOOL), `Definition` (BSTR)
- **Surface**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `IsGenerated` (VARIANT_BOOL), `GeometryType` (SurfaceGeometryType), `StiffnessType` (SurfaceStiffnessType), `MaterialNo` (c_int), `BoundaryLineCount` (c_int), `BoundaryLineList` (BSTR), `Thickness` (SurfaceThickness), `Eccentricity` (c_double), `Area` (c_double), `SetIntegratedObjects` (VARIANT_BOOL), `IntegratedNodeCount` (c_int), `IntegratedNodeList` (BSTR), `IntegratedLineCount` (c_int), `IntegratedLineList` (BSTR), `IntegratedOpeningCount` (c_int), `IntegratedOpeningList` (BSTR), `ControlPoints` (Point3D[])
- **SurfaceAxes**: `No` (c_int), `Direction` (SurfaceAxesDirection), `Rotation` (c_double), `LineList` (BSTR), `Point1` (Point3D), `Point2` (Point3D), `UserCSNo` (c_int)
- **SurfaceBasicStrains**: `SurfaceNo` (c_int), `Type` (ResultsValueType), `LocationNo` (c_int), `Coordinates` (Point3D), `EpsilonXPositive` (c_double), `EpsilonYPositive` (c_double), `GammaXYPositive` (c_double), `EpsilonXNegative` (c_double), `EpsilonYNegative` (c_double), `GammaXYNegative` (c_double)
- **SurfaceBasicStresses**: `SurfaceNo` (c_int), `Type` (ResultsValueType), `LocationNo` (c_int), `Coordinates` (Point3D), `SigmaXPositive` (c_double), `SigmaYPositive` (c_double), `SigmaXNegative` (c_double), `SigmaYNegative` (c_double), `TauXYPositive` (c_double), `TauXYNegative` (c_double), `TauXZ` (c_double), `TauYZ` (c_double)
- **SurfaceContactStresses**: `SurfaceNo` (c_int), `Type` (ResultsValueType), `LocationNo` (c_int), `Coordinates` (Point3D), `StressSigmaZ` (c_double), `StressTauYZ` (c_double), `StressTauXZ` (c_double)
- **SurfaceCrackStrains**: `SurfaceNo` (c_int), `Type` (ResultsValueType), `LocationNo` (c_int), `Coordinates` (Point3D), `EpsilonCXPositive` (c_double), `EpsilonCYPositive` (c_double), `GammaCXYPositive` (c_double), `EpsilonCXNegative` (c_double), `EpsilonCYNegative` (c_double), `GammaCXYNegative` (c_double)
- **SurfaceCriteria**: `SurfaceNo` (c_int), `Type` (ResultsValueType), `LocationNo` (c_int), `Coordinates` (Point3D), `NonlinearityRate` (c_double), `DesignRatio` (c_double), `EquivalentPlasticStrain` (c_double), `EquivalentCrackStrain` (c_double), `StiffnessReduction` (c_double)
- **SurfaceDeformations**: `SurfaceNo` (c_int), `Type` (ResultsValueType), `LocationNo` (c_int), `Coordinates` (Point3D), `TotalDisplacement` (c_double), `Displacements` (Point3D), `Rotations` (Point3D)
- **SurfaceEquivalentStresses**: `SurfaceNo` (c_int), `Type` (ResultsValueType), `LocationNo` (c_int), `Coordinates` (Point3D), `SigmaEqvMax` (c_double), `SigmaEqvPositive` (c_double), `SigmaEqvNegative` (c_double), `SigmaEqvM` (c_double)
- **SurfaceGrid**: `No` (c_int), `Type` (CoordinateSystemType), `Customize` (VARIANT_BOOL), `PointsIn1Positive` (c_int), `PointsIn1Negative` (c_int), `PointsIn2Positive` (c_int), `PointsIn2Negative` (c_int), `AdaptGridDistances` (VARIANT_BOOL), `DistanceIn1` (c_double), `DistanceIn2` (c_double), `Radius` (c_double), `Alpha` (c_double), `Beta` (c_double), `Increment` (c_int), `Origin` (Point3D), `Direction` (Point3D)
- **SurfaceInternalForces**: `SurfaceNo` (c_int), `Type` (ResultsValueType), `LocationNo` (c_int), `Coordinates` (Point3D), `MomentMx` (c_double), `MomentMy` (c_double), `MomentMxy` (c_double), `ShearForceVx` (c_double), `ShearForceVy` (c_double), `AxialForceNx` (c_double), `AxialForceNy` (c_double), `AxialForceNxy` (c_double), `MomentM1` (c_double), `MomentM2` (c_double), `MomentAlphaB` (c_double), `MomentTMaxB` (c_double), `ShearForceVMaxB` (c_double), `ShearForceBetaB` (c_double), `AxialForceN1` (c_double), `AxialForceN2` (c_double), `AxialForceAlphaM` (c_double), `AxialForceVMaxM` (c_double), `MomentMxDPositive` (c_double), `MomentMyDPositive` (c_double), `MomentMcDPositive` (c_double), `MomentMxDNegative` (c_double), `MomentMyDNegative` (c_double), `MomentMcDNegative` (c_double), `AxialForceNxD` (c_double), `AxialForceNyD` (c_double), `AxialForceNcD` (c_double)
- **SurfaceLoad**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `SurfaceList` (BSTR), `Type` (LoadType), `Distribution` (LoadDistributionType), `Direction` (LoadDirectionType), `Node1No` (c_int), `Magnitude1` (c_double), `Node2No` (c_int), `Magnitude2` (c_double), `Node3No` (c_int), `Magnitude3` (c_double), `Magnitude4` (c_double), `Magnitude5` (c_double), `Magnitude6` (c_double), `LoadAxis` (LoadAxis)
- **SurfaceMaximumStrains**: `SurfaceNo` (c_int), `Type` (ResultsValueType), `LocationNo` (c_int), `Coordinates` (Point3D), `EpsilonMaxPositive` (c_double), `EpsilonMinPositive` (c_double), `AbsEpsilonMaxPositive` (c_double), `EpsilonMaxNegative` (c_double), `EpsilonMinNegative` (c_double), `AbsEpsilonMaxNegative` (c_double), `EpsilonMax` (c_double), `EpsilonMin` (c_double), `AbsEpsilonMax` (c_double)
- **SurfaceOtherStresses**: `SurfaceNo` (c_int), `Type` (ResultsValueType), `LocationNo` (c_int), `Coordinates` (Point3D), `SigmaXb` (c_double), `SigmaYb` (c_double), `TauXYb` (c_double), `SigmaXm` (c_double), `SigmaYm` (c_double), `TauXYm` (c_double)
- **SurfacePlasticStrains**: `SurfaceNo` (c_int), `Type` (ResultsValueType), `LocationNo` (c_int), `Coordinates` (Point3D), `EpsilonPXPositive` (c_double), `EpsilonPYPositive` (c_double), `GammaPXYPositive` (c_double), `EpsilonPXNegative` (c_double), `EpsilonPYNegative` (c_double), `GammaPXYNegative` (c_double)
- **SurfacePrincipalStrains**: `SurfaceNo` (c_int), `Type` (ResultsValueType), `LocationNo` (c_int), `Coordinates` (Point3D), `Epsilon1Positive` (c_double), `Epsilon2Positive` (c_double), `AlphaPositive` (c_double), `Epsilon1Negative` (c_double), `Epsilon2Negative` (c_double), `AlphaNegative` (c_double)
- **SurfacePrincipalStresses**: `SurfaceNo` (c_int), `Type` (ResultsValueType), `LocationNo` (c_int), `Coordinates` (Point3D), `Sigma1Positive` (c_double), `Sigma2Positive` (c_double), `AlphaPositive` (c_double), `Sigma1Negative` (c_double), `Sigma2Negative` (c_double), `AlphaNegative` (c_double), `Sigma1m` (c_double), `Sigma2m` (c_double), `AlphaM` (c_double), `TauMax` (c_double)
- **SurfaceStiffness**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `Type` (OrthotropyType), `Rotation` (c_double), `MultiplicationFactors` (StiffnessMultiplicationFactors), `GeometricProperties` (StiffnessGeometricProperties), `Thickness` (c_double), `ConsiderSelfWeight` (VARIANT_BOOL), `SelfWeight` (c_double)
- **SurfaceStiffness2**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `Type` (OrthotropyType), `Rotation` (c_double), `MultiplicationFactors` (StiffnessMultiplicationFactors2), `GeometricProperties` (StiffnessGeometricProperties), `Thickness` (c_double), `ConsiderSelfWeight` (VARIANT_BOOL), `SelfWeight` (c_double)
- **SurfaceStrains**: `SurfaceNo` (c_int), `Type` (ResultsValueType), `LocationNo` (c_int), `Coordinates` (Point3D), `EpsilonPositive` (c_double), `EpsilonNegative` (c_double), `Epsilon` (c_double)
- **SurfaceSupport**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `SurfaceList` (BSTR), `UseSoilin` (VARIANT_BOOL), `SupportConstantX` (c_double), `SupportConstantY` (c_double), `SupportConstantZ` (c_double), `ShearConstantXZ` (c_double), `ShearConstantYZ` (c_double), `SupportNonlinearityZ` (NonlinearityType)
- **SurfaceSupportNonlinearity**: `Type` (SurfaceSupportNonlinearityType), `ContactStress` (c_double), `FrictionCoefficient` (c_double)
- **SurfaceThickness**: `Type` (SurfaceThicknessType), `Constant` (c_double)
- **Tendon**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `Name` (BSTR), `Type` (TendonType), `LineList` (BSTR), `LoadCaseNo` (c_int), `LoadList` (BSTR), `Diameter` (c_double), `Area` (c_double), `StrandsCount` (c_int), `WiresCount` (c_int), `Prestressing` (TendonPrestressType), `PrestressingFrom` (TendonPrestressIndicatorType), `PrestressingProcedure` (TendonPrestressProcedureType), `PrestressingForce` (c_double), `SolverGeo` (BSTR), `SolverSM` (VARIANT_BOOL)
- **TrajectoryLine**: `General` (Line), `GuideLineNo` (c_int), `Rotation` (c_double)
- **TrajectorySurface**: `General` (Surface), `GuideLineNo` (c_int), `StartProfile` (BSTR), `EndProfile` (BSTR), `Rotation` (c_double)
- **UserCoordinateSystem**: `No` (c_int), `ID` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `Name` (BSTR), `OriginNo` (c_int), `Origin` (Point3D), `Point1No` (c_int), `Point1` (Point3D), `Point2No` (c_int), `Point2` (Point3D), `Comment` (BSTR)
- **UserDefinedAxisSystem**: `Type` (UserDefinedAxisSystemType), `RotationSequence` (RotationSequence), `RotationAngles` (Point3D), `ObjectNo` (c_int), `Node1No` (c_int), `Node2No` (c_int), `Axis1` (AxisType), `Axis2` (AxisType)
- **VariableThickness**: `No` (c_int), `ID` (BSTR), `Comment` (BSTR), `Tag` (BSTR), `IsValid` (VARIANT_BOOL), `Node1No` (c_int), `Node2No` (c_int), `Node3No` (c_int), `Thickness1` (c_double), `Thickness2` (c_double), `Thickness3` (c_double)
- **ViewPoint**: `Alpha` (c_double), `Beta` (c_double), `Gamma` (c_double), `PerspectiveFactor` (c_double)
- **Wall**: `Width` (c_double), `Height` (c_double), `MaterialNo` (c_int), `HeadConditions` (SupportConditionsType), `BaseConditions` (SupportConditionsType), `BaseElastic` (c_double), `ActivateShearStiffness` (VARIANT_BOOL)
- **WorkPlane**: `Type` (PlaneType), `OriginNode` (c_int), `OriginCoordinates` (Point3D)

## 3. Aufzählungen

- **ActionCategoryType**: UnknownActionCategory=0, Permanent=1, Prestress=2, Imposed=3, TrafficLoads=4, SnowIce=5, Wind=6, TemperatureNonFire=7, SettlementsOfFoundationSoil=8, OtherCategory=9, Accidental=10, Earthquake=11, UserDefined=12, ImperfectionCategory=13, PermanentSmallFluctuations=14, WeightOfIce=15, DeadLoad=16, DeadLoadDL=17, DeadLoadGK=18, PermanentFromCranes=19, PermanentImposed=20, SelfStrainingForce=21, Variable=22, Live=23, RoofLive=24, ImposedCategoryA=25, ImposedCategoryB=26, ImposedCategoryC=27, ImposedCategoryD=28, ImposedCategoryE=29, ImposedLive=30, ImposedLoad=31, ImposedCategoryF=32, ImposedCategoryG=33, ImposedCategoryH=34, ImposedCategoryI=35, ImposedCategoryJ=36, ImposedLoadsCategoryH=37, ImposedLoadsCategoryK=38, ImposedLoadsCategoryKOther=39, SnowIce2=40, SnowFinland=41, SnowHGreaterThan1000=42, ShowHLowerThan1000=43, SnowSKLowerThan275=44, SnowSKGreaterThan275=45, SnowOutdoorSKLowerThan275=46, SnowOutdoorSKGreaterThan275=47, Snow=48, SnowSweden1=49, SnowSweden2=50, SnowSweden3=51, SnowSaintPierreEtMiquelon=52, SnowIceRain=53, WindLoad=54, WindOnIce=55, WindLiveLoad=56, WindWL=57, WindWK=58, UniformTemperatures=59, TemperatureShrinkageCreep=60, PermanentFromSoilEarthLoad=61, PermanentFromSoilEarthPressure=62, PermanentFromSoilWaterPressure=63, VariableFromSoilEarthPressure=64, VariableFromSoilWaterPressure=65, LateralEarthWaterPressure=66, LateralEarthPressure=67, Fluids=68, Flood=69, Rain=70, CraneLoad=71, ErectionLoad=72, NotionalHorizontalForces=73, ActionsDuringExecution=74, AccidentalLoad=75, EarthquakeLoadE=76, EarthquakeLiveLoad=77, EarthquakeLoadEL=78, GbPermanent=79, GbCivilBuildings211=80, GbCivilBuildings212=81, GbCivilBuildings22=82, GbCivilBuildings231=83, GbCivilBuildings232=84, GbCivilBuildings241=85, GbCivilBuildings242=86, GbCivilBuildings251=87, GbCivilBuildings252=88, GbCivilBuildings261=89, GbCivilBuildings262=90, GbCivilBuildings27=91, GbCivilBuildings281=92, GbCivilBuildings282=93, GbCivilBuildings291=94, GbCivilBuildings292=95, GbCivilBuildings2101=96, GbCivilBuildings2102=97, GbCivilBuildings2111=98, GbCivilBuildings2112=99, GbCivilBuildings2113=100, GbCivilBuildings2121=101, GbCivilBuildings2122=102, GbIndustrialBuilding31=103, GbIndustrialBuilding321=104, GbIndustrialBuilding322=105, GbIndustrialBuilding323=106, GbIndustrialBuilding33=107, GbIndustrialBuilding34=108, GbIndustrialBuilding35=109, GbIndustrialBuilding36=110, GbLiveLoadsOnRoofs41=111, GbLiveLoadsOnRoofs42=112, GbLiveLoadsOnRoofs43=113, GbLiveLoadsOnRoofs44=114, GbAshLoadOnRoofings51=115, GbAshLoadOnRoofings52=116, GbCraneLoads61=117, GbCraneLoads62=118, GbCraneLoads63=119, GbCraneLoads64=120, GbSnowLoadZone1=121, GbSnowLoadZone2=122, GbSnowLoadZone3=123, GbWindLoadSccordingTo714=124, GbAccidentalActions=125, GbSeismic=126, UnevenSettlements=127, Gr1A=128, Gr1B=129, Gr2=130, Gr3=131, Gr4=132, Gr5=133, WindLoadsFwkPersistentDesignSituations=134, WindLoadsFwkExecution=135, WindLoadsFw=136, ConstructionLoadsDueToWorkingPersonnel=137, OtherConstructionLoads=138, ImposedFromCranesCategoryA=139, ImposedFromCranesCategoryB=140, ImposedFromCranesCategoryC=141, ImposedFromCranesCategoryD=142, ImposedFromCranesGeneral=143, PipingSelfWeight=144, PipingFluid=145, PipingFluidPressureTest=146, PipingTemperature=147, PipingPressure=148, PipingTestPressure=149, PipingDisplacement=150, PipingHangerCategory=151, PipingColdSpring=152, FormFindingResults=153, Nbr1A=154, Nbr1B=155, Nbr1C=156, Nbr1D=157, Nbr1E=158, Nbr1F=159, NbrSettlements=160, NbrActionsMaxValues=161, NbrGeneralVariableActions=162, NbrExceptional=163, LoadArisingFromExtraordinaryEvent=164
- **AnalysisMethodType**: UnknownAnalysis=0, GeometricallyLinearStatic=1, SecondOrder=2, LargeDeformation=3, Postcritical=4
- **AreaLoadApplicationType**: FullyClosedPlaneType=0, OnMembersOnlyType=1
- **AreaLoadDistributionType**: AxesOfAnglesType=0, ConstantType=1, CombinedType=2
- **AverageRegionDistributionType**: UnknownAverageRegionDistributionType=0, ThroughAllSurfaces=1, EachSurfaceSeparately=2
- **AverageRegionFormType**: UnknownAverageRegionForm=0, Rectangle=1, Circle=2, Ellipse=3
- **AverageRegionProjectionType**: UnknownAverageRegionProjectionType=0, PerpendicularProjection=1, ProjectionInX=2, ProjectionInY=3, ProjectionInZ=4, ProjectionVector=5
- **AxisType**: UnknownAxis=0, AxisX=1, AxisY=2, AxisZ=3
- **BendingTheoryType**: UnknownTheory=0, MindlingBendingTheory=1, KirchhoffBendingTheory=2
- **ColumnModelType**: UnknownColumnModelType=0, ElasticSurfaceFoundationType=1, ElasticNodeSupportType=2, AdaptedFeMeshType=3
- **ColumnType**: UnknownColumnType=0, RectangularColumnType=1, CircularColumnType=2, LibraryColumnType=3
- **CombinationCriterionType**: UnknownCombinationCriterionType=0, PermanentLoadingType=1, VariableLoadingType=2
- **CommentFrameType**: UnknownFrameType=0, NoneFrameType=1, RectangularFrameType=2, CircularFrameType=3
- **CommentObjectType**: UnknownCommentObjectType=0, GeneralObjectType=1, NodeObjectType=2, LineObjectType=3, MemberObjectType=4
- **CompoundSolidOperationType**: UnknownCompoundType=0, UniteSolidsType=1, SubtractSolidsType=2, IntersectSolidsType=3, FragmentsType=4, ExteriorType=5, InteriorType=6
- **ConnectionSideType**: UnknownConnectionSideType=0, StartSideType=1, EndSideType=2
- **CoordinateSystemType**: UnknownCoordinateSystem=0, Cartesian=1, XCylindrical=2, YCylindrical=3, ZCylindrical=4, Polar=5
- **DataType**: UnknownDataType=0, FloatType=1, IntegerType=2, DoubleType=3, StringType=4
- **DesignSituationType**: UnknownDesignSituation=0, NoneDesignSituation=1, OtherDesignSituation=2, ManualUls=3, ManualUlsAccidental=4, ManualSeismic=5, ManualFire=6, ManualSls=7, UlsEquPermanentTransient=8, UlsEquAccidental=9, UlsEquAccidentalPsi11=10, UlsEquAccidentalPsi21=11, UlsEquAccidentalSnowPsi11=12, UlsEquAccidentalSnowPsi21=13, UlsEquSeismic=14, UlsStaticEquilibriumFundamental=15, UlsStaticEquilibriumAccidental=16, UlsType1Fundamental=17, UlsType1AccidentalPsi11=18, UlsType1AccidentalPsi21=19, UlsStrPermanentTransient610=20, UlsStrPermanentTransient610AAndB=21, UlsStrPermanentTransient610AModB=22, UlsStrAccidental=23, UlsStrAccidentalPsi11=24, UlsStrAccidentalPsi21=25, UlsStrAccidentalShowPsi11=26, UlsStrAccidentalShowPsi21=27, UlsStrSeismic=28, UlsFailureStructureFundamental=29, UlsFailureStructureAccidental=30, UlsType2Fundamental=31, UlsType2AccidentalPsi11=32, UlsType2AccidentalPsi21=33, UlsType3Fundamental=34, UlsType3AccidentalPsi11=35, UlsType3AccidentalPsi21=36, ChinaUlsStaticEquilibriumFundamental=37, ChinaUlsStaticEquilibriumAccidental=38, ChinaUlsStaticEquilibriumSeismic=39, ChinaUlsFailureOfStructureFundamental=40, ChinaUlsFailureOfStructureAccidental=41, ChinaUlsFailureOfStructureSeismic=42, UlsGeoPermanentTransient=43, UlsGeoAccidentalPsi11=44, UlsGeoAccidentalPsi21=45, UlsGeoSeismic=46, SlsCharacteristic=47, SlsFrequent=48, SlsQuasiPermanent=49, SlsServiceability=50, SlsCharacteristic1=51, SlsCharacteristic2=52, SlsEarthquake=53, SlsVibration=54, SlsNonFrequent=55, SlsCharacteristicQuasiPermanent=56, Section23=57, Section231=58, Section232=59, Section233=60, Section234=61, Section235=62, Section236=63, Section237=64, Section24=65, Section241=66, Section242=67, Section243=68, Section244=69, Section245=70, Section246=71, Section247=72, Section248=73, Asce10Section23=74, Asce10Section231=75, Asce10Section232=76, Asce10Section233=77, Asce10Section234=78, Asce10Section235=79, Asce10Section236=80, Asce10Section237=81, Asce10Section24=82, Asce10Section241=83, Asce10Section242=84, Asce10Section243=85, Asce10Section244=86, Asce10Section245=87, Asce10Section246A=88, Asce10Section246B=89, Asce10Section247=90, Asce10Section248=91, Asce10Section25=92, Asce10Section251=93, Asce10Section252=94, Clause722=95, Clause726A=96, Clause726B=97, Clause726C=98, Chapter9=99, Chapter91=100, Chapter92=101, Chapter93=102, Chapter94=103, Chapter95=104, Chapter96=105, Chapter97=106, AppecndixC=107, AppecndixC91=108, AppecndixC92=109, AppecndixC93=110, AppecndixC94=111, AppecndixC95=112, AppecndixC96=113, Chapter5=114, Chapter531A=115, Chapter531B=116, Chapter531C=117, Chapter531D=118, Chapter531E=119, Chapter531F=120, Chapter531G=121, LimitStateOfStrength=122, LimitStateOfStrength1=123, LimitStateOfStrength2=124, LimitStateOfStrength3=125, LimitStateOfStrength4=126, LimitStateOfStrength5=127, LimitStateOfStrength6=128, LimitStateOfServiceability=129, LimitStateOfServiceability1=130, LimitStateOfServiceability2=131, LimitStateOfServiceability3=132, StrengthAndStabilityLimitStates=133, StrengthAndStabilityLimitStates1=134, StrengthAndStabilityLimitStates2=135, StrengthAndStabilityLimitStates3=136, StrengthAndStabilityLimitStates4=137, ServiceabilityLimitState=138, ServiceabilityLimitState1=139, ServiceabilityLimitState2=140, ServiceabilityLimitState3=141, NbccLimitStateOfStrength=142, NbccLimitStateOfStrength1=143, NbccLimitStateOfStrength2=144, NbccLimitStateOfStrength3=145, NbccLimitStateOfStrength4=146, NbccLimitStateOfStrength5=147, NbccLimitStateOfServiceability=148, PipingOperating=149, PipingSustained=150, PipingExpansion=151, PipingOccasional=152, PipingHangerSituation=153, PipingHydroPressureTest=154, NbrUlsNormal=155, NbrUlsSpecial=156, NbrUlsExceptional=157, NbrSlsRare=158, UlsFatigue=159
- **DiagramAfterLastStepType**: UnknownDiagramType=0, TearingDiagramType=1, YieldingDiagramType=2, ContinuousDiagramType=3, StopDiagramType=4
- **DimensionObjectType**: UnknownDimensionObjectType=0, LinearObject=1, ArcLengthObject=2, AngularObject=3, RadialObject=4, SlopeObject=5, HeightObject=6
- **DimensionPlacement**: UnknownDimensionPlacement=0, InnerPlacement=1, OuterPlacement=2, OuterPlacementFromLeftSide=3, OuterPlacementFromRightSide=4
- **DimensionPlaneType**: UnknownDimensionPlaneType=0, FirstPlaneType=1, SecondPlaneType=2, WorkPlaneType=3
- **DimensionReferenceType**: UnknownDimensionReferenceType=0, ReferenceLength=1, DeltaX=2, DeltaY=3, DeltaZ=4
- **DirectionType**: UnknownDirection=0, GlobalDirection=1, LocalDirection=2
- **ErrorType**: UnknownErrorType=0, UserErrorType=1, InternalErrorType=2, WarningType=3, CalculationErrorType=4
- **ExceptionalHandlingType**: UnknownHandlingType=0, NoneHandlingType=1, RemovedFailingMembersType=2, AssignReducedStiffnessType=3
- **FeMeshRefinementType**: UnknownRefinementType=0, NodeCircularType=1, NodeRectangularType=2, LineFeLengthType=3, LineDivisionType=4, LineGraduallyType=5, SurfaceRefinementType=6, SolidRefinementType=7
- **FiniteElementsShape**: UnkownFeShape=0, QuadrangleShapeOnly=1, TriangleShapeOnly=2, TriangleAndQuadrangleShape=3
- **GuideObjectType**: UnknownGuideObject=0, DimensionObject=1, CommentObject=2, CoordinateSystemObject=3, GuidelineObject=4
- **GuidelineType**: UnknownGuidelineType=0, ParallelToX=1, ParallelToY=2, ParallelToZ=3, BiasBy2Points=4, BiasAngleAndPoint=5, PolarGuideline=6
- **HingeSideType**: UnknownSideType=0, NoneSideType=1, LeftSideType=2, RightSideType=3
- **HorizontalAlignmentType**: UnknownHAlignment=0, Left=1, Center=2, Right=3
- **HypothesisType**: UnknownHypothesisType=0, VonMisesHypothesis=1, TrescaHypothesis=2, RankineHypothesis=3, BachHypothesis=4
- **IdenticalObjectsCorrectionType**: DeleteUnusedType=0, UniteType=1
- **IneffectiveFoundationType**: UnknownIneffectivity=0, NoneIneffectivity=1, NegativeConstantStressInZ=2, PositiveConstantStressInZ=3
- **IntegrateStressesAndForcesType**: UnknownIntegration=0, WithinCuboidQuadratic=1, WithinCuboidGeneral=2, WithinCylinder=3, FromIncludeObjects=4
- **ItemAt**: AtIndex=0, AtNo=1
- **LineLoadReferenceType**: UnknownLineLoadReferenceType=0, LinesType=1, ListOfLinesType=2
- **LineReleaseAxisSystem**: UnknownLineReleaseAxisSystem=0, OriginalLineAxisSystem=1, MemberOnOriginalLine=2, ZAxisPerpendicularToSurface=3, HelpNodeAxisSystem=4
- **LineType**: UnknownLineType=0, PolylineType=1, SplineType=2, CircleType=3, ArcType=4, BSplineType=5, BezierSplineType=6, IntersectionType=7, TrajectoryType=8, OnSurfaceType=9, EllipseType=10, EllipticalArcType=11, ParabolaType=12, HyperbolaType=13, NurbSplineType=14, CopyType=15
- **LoadAxisDefinitionType**: UnknownLoadAxisDefinitionType=0, PointAndAxisType=1, TwoPointsType=2
- **LoadAxisType**: UnknownLoadAxisType=0, PositiveAxisXType=1, PositiveAxisYType=2, PositiveAxisZType=3, NegativeAxisXType=4, NegativeAxisYType=5, NegativeAxisZType=6
- **LoadDefinitionType**: UnknownLoadDefinitionType=0, ByComponentsType=1, ByDirectionType=2
- **LoadDirectionType**: UnknownLoadDirectionType=0, GlobalXType=1, GlobalYType=2, GlobalZType=3, LocalXType=4, LocalYType=5, LocalZType=6, LocalUType=7, LocalVType=8, ProjectXType=9, ProjectYType=10, ProjectZType=11, PerpendicularZType=12
- **LoadDistributionType**: UnknownLoadDistributionType=0, ConcentratedType=1, ConcentratedNxQType=2, Concentrated2x2QType=3, Concentrated2xQType=4, ConcentratedUserDefinedType=5, UniformType=6, TrapezoidalType=7, TaperedType=8, ParabolicType=9, VaryingType=10, LinearType=11, LinearXType=12, LinearYType=13, LinearZType=14, RadialType=15
- **LoadObjectType**: UnknownLoadObject=0, NodalLoadObject=1, MemberLoadObject=2, LineLoadObject=3, SurfaceLoadObject=4, SolidLoadObject=5, FreeConcentratedLoadObject=6, FreeLineLoadObject=7, FreeRectangularLoadObject=8, FreeCircularLoadObject=9, FreePolygonLoadObject=10, FreeVariableLoadObject=11, ImposedNodalDeformationObject=12, ImposedLineDisplacementObject=13, ImperfectionObject=14
- **LoadType**: UnknownLoadType=0, ForceType=1, MomentType=2, TemperatureType=3, AxialStrainType=4, AxialDisplacementType=5, PrecamberType=6, InitialPrestressType=7, EndPrestressType=8, DisplacementType=9, RotationLoadType=10, FullPipeContentType=11, PartialPipeContentType=12, PipeInternalPressureType=13, RotaryMotionType=14, BuoyancyType=15
- **LoadingType**: UnknownLoadingType=0, LoadCaseType=1, LoadCombinationType=2, ResultCombinationType=3, SuperCombinationType=4, DynamicCaseType=5, DynamicCombinationType=6, ModuleCaseType=7
- **MaterialModelDefinitionType**: UnknownModelDefinitionType=0, BasicDefinitionType=1, BilinearDefinitionType=2, DiagramDefinitionType=3
- **MaterialModelType**: UnknownMaterialModelType=0, IsotropicLinearElasticType=1, IsotropicNonlinearElastic1DType=2, IsotropicNonlinearElastic2D3DType=3, IsotropicPlastic1DType=4, IsotropicPlastic2D3DType=5, OrthotropicElastic2DType=6, OrthotropicElastic3DType=7, OrthotropicPlastic2DType=8, OrthotropicPlastic3DType=9, TransverselyIsotropicElastic3DType=10, IsotropicThermalElasticType=11, IsotropicMasonry2D=12
- **MaterialStrainHypothesisType**: UnknownStrainHypothesisType=0, NoneHypothesisType=1, VonMisesHypothesisType=2, TrescaHypothesisType=3, DruckerPragerHypothesisType=4, MohrCoulombHypothesisType=5
- **MemberAxesType**: UnknownAxesType=0, GlobalAxes=1, LocalMemberAxes=2, LocalPrincipalAxes=3
- **MemberLoadReferenceType**: UnknownMemberLoadReferenceType=0, MembersType=1, ListOfMembersType=2, SetsOfMembersType=3
- **MemberNonlinearityType**: UnknownMemberNonlinearityType=0, FailureTensionType=1, FailureCompressionType=2, FailureTensionSlippageType=3, FailureCompressionSlippageType=4, SlippageType=5, TearingTensionType=6, YieldingTensionType=7, TearingCompressionType=8, YieldingCompressionType=9, TearingType=10, YieldingType=11, MemberPlasticHingeType=12
- **MemberType**: UnknownMemberType=0, Beam=1, Rigid=2, RibType=3, Truss=4, TrussOnlyN=5, Tension=6, Compression=7, Buckling=8, Cable=9, CableOnPulleys=10, ResultBeamType=11, DefinableStiffness=12, CouplingRigidRigid=13, CouplingRigidHinge=14, CouplingHingeHinge=15, CouplingHingeRigid=16, Spring=17, NullMember=18
- **ModelObjectType**: UnknownObject=0, NodeObject=1, LineObject=2, MaterialObject=3, SurfaceObject=4, SolidObject=5, OpeningObject=6, CavityObject=7, NodalSupportObject=8, LineSupportObject=9, SurfaceSupportObject=10, LineHingeObject=11, CrossSectionObject=12, MemberHingeObject=13, MemberEccentricityObject=14, MemberDivisionObject=15, MemberObject=16, RibObject=17, MemberElasticFoundationObject=18, MemberNonlinearityObject=19, SetOfMembersObject=20, IntersectionOfSurfacesObject=21, IntersectionOfSolidsObject=22, FeMeshRefinementObject=23, NodalReleaseObject=24, LineReleaseTypeObject=25, LineReleaseObject=26, ConnectionEccentricityObject=27, ConnectionOfTwoMembersObject=28, JointObject=29, TendonObject=30
- **ModelType**: UnknownModel=0, Model3D=1, Model2DPlateXY=2, Model2DWallXZ=3, Model2DWallXY=4
- **NodalLoadDirectionType**: UnknownNodalLoadDirectionType=0, RotatedDirectionType=1, CoordinateSystemDirectionType=2, DirectToNodeType=3, TwoNodesDirectionType=4, SameAsMemberDirectionType=5, SameAsLineDirectionType=6
- **NodalReleaseAxisSystem**: UnknownNodalReleaseAxisSystem=0, GlobalAxisSystem=1, LocalFromMember=2, LocalFromLine=3
- **NodeType**: UnknownNode=0, Standard=1, NodeOnLine=2, NodeOnSurface=3, TrajectoryNode=4, Parameterized=5
- **NonlinearityDirectionType**: UnknownDirectionType=0, AlongAxisX=1, AlongAxisY=2, AlongAxisZ=3, AroundAxisX=4, AroundAxisY=5, AroundAxisZ=6
- **NonlinearityType**: UnknownNonlinearityType=0, NoneNonlinearityType=1, FailureIfNegativeType=2, FailureIfPositiveType=3, FailureAllIfNegativeType=4, FailureAllIfPositiveType=5, PartialActivityNLType=6, WorkingDiagramType=7, FrictionAType=8, FrictionBType=9, FrictionCType=10, FrictionDType=11, StiffnessDiagramType=12, ScaffoldingType=13, FormFindingType=14, FixedIfNegativeType=15, FixedIfPositiveType=16, PlasticHingeNLType=17, ScaffoldingDiagramType=18
- **OrientationType**: Downward=0, Upward=1
- **OrthotropyType**: UnknownOrthotropyType=0, ConstantThickness=1, EffectiveThickness=2, DefinedByStiffnessMatrix=3, Coupling=4, UnidirectionalRibbedPlate=5, BidirectionalRibbedPlate=6, TrapezoidalSheet=7, HollowCoreSlab=8, Grillage=9, UnidirectionalBoxFloor=10, Glass=11, Laminate=12
- **ParallelContactType**: UnknownParallelContactType=0, FailureIfPerpendicularContactFailed=1, ParallelFullForceTransmissionType=2, RigidFrictionType=3, RigidFictionLimitType=4, ElasticFrictionType=5, ElasticFrictionLimitType=6, ElasticSolidBehaviorType=7
- **PartialActivityType**: UnknownPartialActivityType=0, CompleteActivityType=1, FixedActivityType=2, TearingActivityType=3, YieldingActivityType=4, FailureActivityType=5
- **PerpendicularContactType**: UnknownPerpendicularContactType=0, PerpendicularFullForceTransmissionType=1, FailureUnderCompression=2, FailureUnderTension=3
- **PlaneType**: UnknownPlane=0, PlaneXY=1, PlaneYZ=2, PlaneXZ=3
- **PlasticHingeAcceptanceCriteriaType**: UnknownPlasticHingeAcceptanceCriteriaType=0, PrimaryPlasticHingeAcceptanceCriteriaType=1, SecondaryPlasticHingeAcceptanceCriteriaType=2
- **PlasticHingeType**: UnknownPlasticHingeType=0, Fema356UserDefinedType=1, BilinearUserDefinedType=2, Fema356RigidPlasticAutomaticType=3, Fema356ElasticPlasticAutomatic=4, BilinearAutomaticType=5
- **PrecamberActivityCriterionType**: UnknownPrecamberActivityCriterionType=0, ActivityAlways=1, ActivityAccording_EN_1993_1_1=2, ActivityAccording_DIN_18800_2=3, ActivityManually=4
- **ProtocolDateType**: UnknownProtocolDateType=0, DateOfLastModificationType=1, TodayDateType=2, UserDefinedDateType=3
- **QuadraticCombinationType**: UnknownQuadraticCobminationType=0, PositiveNegative=1, Positive=2, Negative=3
- **RadialDimensionType**: UnknownRadialDimensionType=0, RadiusType=1, DiameterType=2
- **RadialDimensionViewType**: UnknownRadialDimensionViewType=0, ViewFromCenter=1, PartViewAbsolutely=2, PartViewRelatively=3
- **ReferenceSystemType**: UnknownReferenceSystemType=0, GlobalSystemType=1, LocalSystemType=2, UserDefinedSystemType=3
- **ReferenceType**: UnknownReferenceType=0, RelativeReferenceType=1, AbsoluteReferenceType=2
- **ReleaseLocation**: UnknownReleaseLocatonType=0, OriginalLocationType=1, ReleaseLocationType=2
- **ResultsDistributionType**: ConstantDistributionOnElements=0, NonContinuousDistribution=1, ContinuousDistributionWithinObjects=2, ContinuousDistributionTotal=3, ContinuousDistributionByGroup=4
- **ResultsFlag**: UnknownFlag=0, StandardValueFlag=1, LeftSideFlag=2, RightSideFlag=3, GraphicsResultsFlag=4, NumbericResultsFlag=5
- **ResultsType**: UnknownResultsType=0, GlobalDeformationU=1, GlobalDeformationX=2, GlobalDeformationY=3, GlobalDeformationZ=4, GlobalDeformationPhiX=5, GlobalDeformationPhiY=6, GlobalDeformationPhiZ=7, LocalDeformationX=8, LocalDeformationY=9, LocalDeformationZ=10, LocalDeformationPhiX=11, LocalDeformationPhiY=12, LocalDeformationPhiZ=13, CriteriaNonlinearityRate=14, CriteriaDesignRatio=15, CriteriaEquivalentPlasticStrain=16, CriteriaEquivalentFracturingStrain=17, CriteriaPositiveCrackDirections=18, CriteriaNegativeCrackDirections=19, CriteriaDamageParameter=20, CriteriaStiffnessReduction=21, CriteriaEnergyError=22, MomentMx=23, MomentMy=24, MomentMxy=25, ShearForceVx=26, ShearForceVy=27, AxialForceNx=28, AxialForceNy=29, AxialForceNxy=30, MomentM1=31, MomentM2=32, MomentAlphaB=33, MomentTMaxB=34, ShearForceVMaxB=35, ShearForceBetaB=36, AxialForceN1=37, AxialForceN2=38, AxialForceAlphaM=39, AxialForceVMaxM=40, MomentMxDPositive=41, MomentMyDPositive=42, MomentMcDPositive=43, MomentMxDNegative=44, MomentMyDNegative=45, MomentMcDNegative=46, AxialForceNxD=47, AxialForceNyD=48, AxialForceNcD=49, StressSigmaXPositive=50, StressSigmaYPositive=51, StressTauXYPositive=52, StressSigmaXNegative=53, StressSigmaYNegative=54, StressTauXYNegative=55, StressSigma1Positive=56, StressSigma2Positive=57, StressAlphaPositive=58, StressSigma1Negative=59, StressSigma2Negative=60, StressAlphaNegative=61, StressSigma1m=62, StressSigma2m=63, StressAlphaM=64, StressTauMax=65, StressSigmaZ=66, StressSigmaXb=67, StressSigmaYb=68, StressTauXYb=69, StressSigmaXm=70, StressSigmaYm=71, StressTauXYm=72, StressTauXZ=73, StressTauYZ=74, StressSigmaEqvMaxMises=75, StressSigmaEqvPositiveMises=76, StressSigmaEqvNegativeMises=77, StressSigmaEqvMMises=78, StressSigmaEqvMaxTresca=79, StressSigmaEqvPositiveTresca=80, StressSigmaEqvNegativeTresca=81, StressSigmaEqvMTresca=82, StressSigmaEqvMaxRankine=83, StressSigmaEqvPositiveRankine=84, StressSigmaEqvNegativeRankine=85, StressSigmaEqvMRankine=86, StressSigmaEqvMaxBach=87, StressSigmaEqvPositiveBach=88, StressSigmaEqvNegativeBach=89, StressSigmaEqvMBach=90, ContactStressSigmaZ=91, ContactStressTauYZ=92, ContactStressTauXZ=93, StrainEpsilonXPositive=94, StrainEpsilonYPositive=95, StrainGammaXYPositive=96, StrainEpsilonXNegative=97, StrainEpsilonYNegative=98, StrainGammaXYNegative=99, StrainEpsilon1Positive=100, StrainEpsilon2Positive=101, StrainAlphaPositive=102, StrainEpsilon1Negative=103, StrainEpsilon2Negative=104, StrainAlphaNegative=105, StrainEpsilonMaxPositive=106, StrainEpsilonMinPositive=107, StrainAbsEpsilonMaxPositive=108, StrainEpsilonMaxNegative=109, StrainEpsilonMinNegative=110, StrainAbsEpsilonMaxNegative=111, StrainEpsilonMax=112, StrainEpsilonMin=113, StrainAbsEpsilonMax=114, StrainEpsilonPositiveMises=115, StrainEpsilonNegativeMises=116, StrainEpsilonMises=117, StrainEpsilonPositiveTresca=118, StrainEpsilonNegativeTresca=119, StrainEpsilonTresca=120, StrainEpsilonPositiveRankine=121, StrainEpsilonNegativeRankine=122, StrainEpsilonRankine=123, StrainEpsilonPositiveBach=124, StrainEpsilonNegativeBach=125, StrainEpsilonBach=126, IsotropicParameterE=127, IsotropicParameterMi=128, IsotropicParameterD=129, PlasticStrainEpsilonPXPositive=130, PlasticStrainEpsilonPYPositive=131, PlasticStrainGammaPXYPositive=132, PlasticStrainEpsilonPXNegative=133, PlasticStrainEpsilonPYNegative=134, PlasticStrainGammaPXYNegative=135, FracturingStrainEpsilonFXPositive=136, FracturingStrainEpsilonFYPositive=137, FracturingStrainGammaFXYPositive=138, FracturingStrainEpsilonFXNegative=139, FracturingStrainEpsilonFYNegative=140, FracturingStrainGammaFXYNegative=141, StressSigmaX=142, StressSigmaY=143, StressTauXY=144, StressSigmaV=145, StressSigma1=146, StressSigma2=147, StressSigma3=148, StressSigma123=149, StressSigmaVMises=150, StressSigmaVRankine=151, StressSigmaVTresca=152, StressSigmaVBach=153, StrainEpsilonX=154, StrainEpsilonY=155, StrainEpsilonZ=156, StrainGammaYZ=157, StrainGammaXZ=158, StrainGammaXY=159, StrainEpsilon1=160, StrainEpsilon2=161, StrainEpsilon3=162, StrainEpsilon123=163, PlasticStrainEpsilonPX=164, PlasticStrainEpsilonPY=165, PlasticStrainEpsilonPZ=166, PlasticStrainGammaPYZ=167, PlasticStrainGammaPXZ=168, PlasticStrainGammaPXY=169
- **ResultsValueType**: UnknownValueType=0, StandardValueType=1, MaximumValueType=2, MinimumValueType=3, MaximumAlongX=4, MinimumAlongX=5, MaximumAlongY=6, MinimumAlongY=7, MaximumAlongZ=8, MinimumAlongZ=9, MaximumAroundX=10, MinimumAroundX=11, MaximumAroundY=12, MinimumAroundY=13, MaximumAroundZ=14, MinimumAroundZ=15
- **RibPositionType**: UnknownRibPosition=0, OnPositiveSide=1, OnNegativeSide=2, InCenter=3, UserDefinedPosition=4
- **RotationSequence**: UnknownRotationSequence=0, SequenceZYX=1, SequenceZXY=2, SequenceYZX=3, SequenceYXZ=4, SequenceXZY=5, SequenceXYZ=6
- **RotationType**: UnknownRotation=0, NoneRotation=1, Angle=2, HelpNode=3
- **ScaffoldingDefinitionType**: UnknownScaffoldingType=0, AbsoluteDefinitionType=1, RelativeDefinitionType=2
- **ScalingDirectionType**: UnknownScalingDirection=0, AllDirections=1, DefinedDirection=2, DefinedDirectionBy2Points=3
- **SectionPlaneType**: UnknownSectionPlaneType=0, LocalPlaneInPositiveZ=1, LocalPlaneInNegativeZ=2, LocalPlaneInPositiveY=3, LocalPlaneInNegativeY=4, GlobalPlaneInPositiveX=5, GlobalPlaneInNegativeX=6, GlobalPlaneInPositiveY=7, GlobalPlaneInNegativeY=8, GlobalPlaneInPositiveZ=9, GlobalPlaneInNegativeZ=10
- **SectionType**: UnknownSectionType=0, SectionViaSurfacePlane=1, SectionOnSurfaceLine=2, SectionOnSolidSectionLine=3, SectionOnSolidBoundarySurfaces=4, SectionOnSectionalArea=5
- **SelfWeightType**: UnknownSelfWeightType=0, Weight=1, WeightPerLength=2, SpecificWeightAndCrScArea=3
- **SetOfMembersType**: UnknownSet=0, ContinuousMembers=1, GroupOfMembers=2
- **SolidAxesDirection**: UnknownSolidAxesDirection=0, StandardSolidAxesDirection=1, SolidAxesXYParallelToSurface=2, SolidAxisXParallelToLine=3, SolidAxisYParallelToLine=4, SolidAxisXParallelToSurface=5, SolidAxisYParallelToSurface=6, SolidAxesParallelToUserCS=7
- **SolidType**: UnknownSolidType=0, MaterialSolidType=1, GasSolidType=2, ContactSolidType=3, NullSolidType=4
- **SolverMethodType**: UnknownSolverMethod=0, DirectSolverMethod=1, IterativeSolverMethod=2
- **SolverVersionType**: UnknownSolverVersionType=0, Solver32Type=1, Solver64Type=2
- **SolvingSystemMethodType**: UnknownSolvingSystem=0, NewtonRaphson=1, NewtonRaphsonPicard=2, Picard=3, NewtonRaphsonConstantMatrix=4, ModifiedNewtonRaphson=5, DynamicRelaxation=6
- **SpringDefinitionType**: UnknownDefinitionType=0, ParametersDefinition=1, DiagramDefinition=2
- **SpringLimitsType**: UnknownLimitsType=0, NoLimits=1, Deformation=2, Force=3
- **StiffnessDiagramForceType**: UnknownStiffnessForceType=0, NoneStiffnessForce=1, StiffnessForceXType=2, StiffnessForceYType=3, StiffnessForceZType=4, StiffnessForceAbsType=5
- **StoppingConditionType**: UnknownStoppingConditionType=0, NoneStoppingConditionType=1, UType=2, UXType=3, UYType=4, UZType=5, PhiType=6, PhiXType=7, PhiYType=8, PhiZType=9
- **SupportConditionsType**: UnknownSupportConditionType=0, HingedSupportType=1, ElasticSupportType=2, RigidSupportType=3
- **SurfaceAxesDirection**: UnknownSurfaceAxesDirection=0, StandardSurfaceAxesDirection=1, IdenticalToAxesForInput=2, SurfaceAngularRotation=3, SurfaceAxisXParallelToLine=4, SurfaceAxisYParallelToLine=5, SurfaceAxisXDirectToPoint=6, SurfaceAxisYDirectToPoint=7, SurfaceAxesParallelToGlobalCS=8, SurfaceAxesParallelToUserCS=9
- **SurfaceGeometryType**: UnknownGeometryType=0, PlaneSurfaceType=1, QuadrangleSurfaceType=2, BSplineSurfaceType=3, RotatedSurfaceType=4, PipeSurfaceType=5, TrajectorySurfaceType=6, NurbsSurfaceType=7, MinimumCurvatureSurfaceType=8, PartialSurfaceType=9, ComponentSurfaceType=10
- **SurfaceStiffnessType**: UnknownStiffnessType=0, StandardStiffnessType=1, WithoutTensionStiffnessType=2, OrthotropicStiffnessType=3, GlassStiffnessType=4, LaminateStiffnessType=5, RigidStiffnessType=6, MembraneStiffnessType=7, MembraneOrthotropicStiffnessType=8, NullStiffnessType=9
- **SurfaceSupportNonlinearityType**: UnknownSurfaceNonlinearityType=0, BasicUnidirectionalActionType=1, YieldingFromContactStressType=2, FrictionInPlaneType=3
- **SurfaceThicknessType**: UnknownThicknessType=0, ConstantThicknessType=1, VariableThicknessType=2
- **TaperShapeType**: UnknownTaperShape=0, NoneTaper=1, Linear=2, Quadratic=3
- **TendonPrestressIndicatorType**: FromUnknown=0, FromBegin=1, FromEnd=2, FromBothAnchorBegin=3, FromBothAnchorEnd=4
- **TendonPrestressProcedureType**: UnknownProcedure=0, ProcedureType1=1, ProcedureType2=2, ProcedureType3=3, ProcedureType4=4, ProcedureType5=5
- **TendonPrestressType**: UnknownPrestress=0, BondedTendon=1, PretensionedTendon=2
- **TendonType**: UnknownTendon=0, StrandTendon=1, WireTendon=2, BarTendon=3
- **ToolType**: SelectNodes=0, SelectLines=1, SelectSurfaces=2, SelectSolids=3, SelectOpenings=4, SelectMembers=5, SelectSetsOfMembers=6
- **UnitType**: UnknownUnitType=0, LengthUnitType=1, AreaUnitType=2, AngleUnitType=3, SurfaceThicknessUnitType=4, CrossSectionalDimensionUnitType=5, EGModuleUnitType=6, SpecificWeightUnitType=7, CoefficientOfThermalExpansionUnitType=8, WeightPerLengthUnitType=9, AreaPerLengthUnitType=10, NodalTranslationalSpringUnitType=11, NodalRotationalSpringUnitType=12, LineTranslationalSpringUnitType=13, LineShearSpringUnitType=14, LineRotationalSpringUnitType=15, SurfaceTranslationalSpringUnitType=16, SurfaceShearSpringUnitType=17, MomentOfInertiaUnitType=18, CrossSectionalAreasUnitType=19, ForceUnitType=20, StressUnitType=21, MomentUnitType=22, LineMomentUnitType=23, LineForceUnitType=24, ForcePerAreaUnitType=25, TemperatureUnitType=26, AxialStrainUnitType=27, PrecamberUnitType=28, InternalPressureUnitType=29, DisplacementUnitType=30, RotationUnitType=31, TimeUnitType=32, MassUnitType=33, PercentUnitType=34, DimensionlessUnitType=35, CrossSectionUnitType=36, SolidLoadsUnitType=37, AngularVelocitiesUnitType=38, AngularAccelerationsUnitType=39
- **UserDefinedAxisSystemType**: UnknownSystemType=0, RotatedSystemType=1, DefinedCoordinateSystemType=2, TwoNodesType=3, ThreeNodesType=4, SameAsMemberType=5, SameAsLineType=6
- **VerticalAlignmentType**: UnknownVAlignment=0, Top=1, Middle=2, Bottom=3

"""global strings"""
BOMS_PKL_PATH = "\\AppData\\Roaming\\PROJECTEXPLORER\\boms.pkl"

BOM_SQL_STRING_PRE = (
    "WITH myCTE (Parent, Child, Balloon, listASP, \n"
    "Name, PurNo, Qty, Rev, Level, Path) \n"
    'AS (\n'
    'SELECT cast(\'\' as nvarchar(20)) AS Parent, \n'
    'list.HINBAN AS Child, \n'
    'cast(\'\' as nvarchar(3)) as Balloon, \n'
    'list.ASP_KBN as listASP, \n'
    'list.HINMEI as Name, \n'
    'list.YOBI_KATASHIKI as PurNo, \n'
    'cast(0 as decimal(10,5)) as Qty, \n'
    'list.MATSUBI as Rev, \n'
    '0 as Level, \n'
    'cast(\'\' as nvarchar(200)) as Path \n'
    'FROM MATIX_E_BOM_LIST AS list \n'
    'WHERE list.HINBAN = \''
    )

BOM_SQL_STRING_POST = (
    '\' UNION ALL \n'
    'SELECT tree.OYA_HINBAN as Parent, \n'
    'tree.KO_HINBAN AS Child, \n'
    'tree.FUGOH AS Balloon, \n'
    'list.ASP_KBN as listASP, \n'
    'list.HINMEI as Name, \n'
    'list.YOBI_KATASHIKI as PurNo, \n'
    'cast(tree.SURYO as decimal(10,5)) as Qty, \n'
    'list.MATSUBI as Rev, \n'
    'Level + 1, cast((Path + tree.OYA_HINBAN + ISNULL(tree.FUGOH,\'000\')) as nvarchar(200)) \n'
    'FROM MATIX_E_BOM_TREE AS tree \n'
    'INNER JOIN MATIX_E_BOM_LIST AS list \n'
    'ON tree.KO_HINBAN = list.HINBAN \n'
    'INNER JOIN myCTE AS c \n'
    'ON tree.OYA_HINBAN = c.Child \n'
    ') \n'
    'SELECT myCTE.*, FileIndex.* \n'
    'FROM myCTE \n'
    'LEFT JOIN FileIndex \n'
    'ON myCTE.Child = FileIndex.Mnumber \n'
    'ORDER BY Path, Balloon, FileName; \n'
    )

BOMS_SQL_STRING = '''
    SELECT [MATIX_E_BOM_LIST].HINBAN AS 'M-Number',
    [MATIX_E_BOM_LIST].HINMEI as 'Job Name',
    [MATIX_E_BOM_LIST].YOBI_KATASHIKI, 
    [MATIX_E_BOM_LIST].MATSUBI,
    [MATIX_E-JOB_NO].DESIGN_NO as 'Job Number' 
    FROM [MATIX_E_BOM_LIST] LEFT OUTER JOIN 
    [MATIX_E-JOB_NO] ON [MATIX_E_BOM_LIST].HINBAN like [MATIX_E-JOB_NO].HINBAN 
    WHERE [MATIX_E_BOM_LIST].ASP_KBN = 'A' 
    ORDER BY CASE WHEN DESIGN_NO IS NULL THEN 1 ELSE 0 END, DESIGN_NO;
    '''

BOM_SQL_STRING_PRE_TESTx = (
    "WITH myCTE (Parent, Child, Balloon, listASP, \n"
    "Name, PurNo, Qty, Rev, Level, Path, Position) \n"
    'AS (\n'
    'SELECT cast(\'\' as nvarchar(20)) AS Parent, \n'
    'list.HINBAN AS Child, \n'
    'cast(\'\' as nvarchar(3)) as Balloon, \n'
    'list.ASP_KBN as listASP, \n'
    'list.HINMEI as Name, \n'
    'list.YOBI_KATASHIKI as PurNo, \n'
    'cast(0 as decimal(10,5)) as Qty, \n'
    'list.MATSUBI as Rev, \n'
    '0 as Level, \n'
    'cast(\'\' as nvarchar(200)) as Path, \n'
    'cast(ROW_NUMBER() OVER (ORDER BY list.HINBAN) as nvarchar(200)) as Position \n'
    'FROM MATIX_E_BOM_LIST AS list \n'
    'WHERE list.HINBAN = \''
)

BOM_SQL_STRING_POST_TESTx = (
    '\' UNION ALL \n'
    'SELECT tree.OYA_HINBAN as Parent, \n'
    'tree.KO_HINBAN AS Child, \n'
    'tree.FUGOH AS Balloon, \n'
    'list.ASP_KBN as listASP, \n'
    'list.HINMEI as Name, \n'
    'list.YOBI_KATASHIKI as PurNo, \n'
    'cast(tree.SURYO as decimal(10,5)) as Qty, \n'
    'list.MATSUBI as Rev, \n'
    'Level + 1, \n'
    'cast((Path + tree.OYA_HINBAN + ISNULL(tree.FUGOH,\'000\')) as nvarchar(200)), \n'
    'cast(c.Position + \'.\' + cast(ROW_NUMBER() OVER (PARTITION BY tree.OYA_HINBAN ORDER BY tree.KO_HINBAN) as nvarchar(200)) as nvarchar(200)) as Position \n'
    'FROM MATIX_E_BOM_TREE AS tree \n'
    'INNER JOIN MATIX_E_BOM_LIST AS list \n'
    'ON tree.KO_HINBAN = list.HINBAN \n'
    'INNER JOIN myCTE AS c \n'
    'ON tree.OYA_HINBAN = c.Child \n'
    ') \n'
    'SELECT myCTE.*, FileIndex.* \n'
    'FROM myCTE \n'
    'LEFT JOIN FileIndex \n'
    'ON myCTE.Child = FileIndex.Mnumber \n'
    'ORDER BY Path, Balloon, FileName; \n'
)

BOM_SQL_STRING_PRE_TEST = (
    "WITH myCTE (Parent, Child, Balloon, listASP, \n"
    "Name, PurNo, Qty, Rev, Level, Path, Position) \n"
    'AS (\n'
    'SELECT cast(\'\' as nvarchar(20)) AS Parent, \n'
    'list.HINBAN AS Child, \n'
    'cast(\'\' as nvarchar(3)) as Balloon, \n'
    'list.ASP_KBN as listASP, \n'
    'list.HINMEI as Name, \n'
    'list.YOBI_KATASHIKI as PurNo, \n'
    'cast(0 as decimal(10,5)) as Qty, \n'
    'list.MATSUBI as Rev, \n'
    '0 as Level, \n'
    'cast(\'\' as nvarchar(200)) as Path, \n'
    'cast(ROW_NUMBER() OVER (ORDER BY list.HINBAN) as nvarchar(200)) as Position \n'
    'FROM MATIX_E_BOM_LIST AS list \n'
    'WHERE list.HINBAN = \''  # Ensure to close the string and add the variable for the item
)

BOM_SQL_STRING_POST_TEST = (
    '\' UNION ALL \n'
    'SELECT tree.OYA_HINBAN as Parent, \n'
    'tree.KO_HINBAN AS Child, \n'
    'tree.FUGOH AS Balloon, \n'
    'list.ASP_KBN as listASP, \n'
    'list.HINMEI as Name, \n'
    'list.YOBI_KATASHIKI as PurNo, \n'
    'cast(tree.SURYO as decimal(10,5)) as Qty, \n'
    'list.MATSUBI as Rev, \n'
    'Level + 1, \n'
    'cast((Path + \'.\' + cast(ROW_NUMBER() OVER (PARTITION BY c.Child ORDER BY tree.KO_HINBAN) as nvarchar(200))) as nvarchar(200)), \n'
    'cast(c.Position + \'.\' + cast(ROW_NUMBER() OVER (PARTITION BY c.Child ORDER BY tree.KO_HINBAN) as nvarchar(200)) as nvarchar(200)) as Position \n'
    'FROM MATIX_E_BOM_TREE AS tree \n'
    'INNER JOIN MATIX_E_BOM_LIST AS list \n'
    'ON tree.KO_HINBAN = list.HINBAN \n'
    'INNER JOIN myCTE AS c \n'
    'ON tree.OYA_HINBAN = c.Child \n'
    ') \n'
    'SELECT myCTE.*, FileIndex.* \n'
    'FROM myCTE \n'
    'LEFT JOIN FileIndex \n'
    'ON myCTE.Child = FileIndex.Mnumber \n'
    'ORDER BY Path, Balloon, FileName; \n'
)

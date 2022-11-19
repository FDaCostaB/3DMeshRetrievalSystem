import sys
import os
import DBData as db
import LP as lp
import featureName
from Mesh import Mesh
from Settings import readSettings
from tsne import tsne
import warnings

warnings.filterwarnings("ignore")
readSettings()

if len(sys.argv) == 2:
    """Normalizing the initial database

       Step of the assignment
       -----------------------
        Step 3

       Command
       -------
        main.py full-normalisation

       Parameters
       ----------
        None

       Returns/Output
       -------
        Export each normalized 3d mesh of the <DATABASE FOLDER> in the <OUTPUT FOLDER>/NormaliseDB/ """
    if sys.argv[1] == "full-normalisation":
        db.normalise()

    """Export extracted features of all 3D mesh of the normalized database located at <OUTPUT FOLDER>/NormaliseDB/
       Requires :
        Normalized database located at <OUTPUT FOLDER>/NormaliseDB/ given by "main.py full-normalisation"

       Step of the assignment
       -----------------------
        Step 3

       Command
       -------
        main.py features

       Parameters
       ----------
        None

       Returns/Output
       --------------
        A list containing for each object of the normalized DB of a dictionary containing the feature extract from the mesh
        Export a CSV containing properties of each object of the database given in parameter """
    if sys.argv[1] == "features":
        db.exportDBFeatures()

    """Measure time taken by 380 queries (each object of the DB queried once)
       Requires :
        Normalized database located at <OUTPUT FOLDER>/NormaliseDB/ given by "main.py full-normalisation"

       Step of the assignment
       -----------------------
        Step 5 (compare ANN)

       Command
       -------
        main.py time

       Parameters
       ----------
        None

       Returns/Output
       --------------
        Print in the command line Min, Max, Mean, Standard deviation, Median taken by 380 queries (each object of the DB queried once)"""
    if sys.argv[1] == "time":
        db.timeQuery()

    """Measure efficiency of the retrieval system regarding different metrics
       Requires :
        Normalized database located at <OUTPUT FOLDER>/NormaliseDB/ given by "main.py full-normalisation"

       Step of the assignment
       -----------------------
        Step 6

       Command
       -------
        main.py evaluate

       Parameters
       ----------
        None

       Returns/Output
       --------------
        Export CSV reporting TP, FP, TN, FN, Total performance, Accuracy, Recall/Sensitivity, Specificity, AUROC for a query for each mesh
        Allow computations of different statistics in a sheet editor """
    if sys.argv[1] == "evaluate":
        db.evaluateQuery()

    """Compute the optimised integer weight for each features to improve the global performance of the retrieval system
    (i.e. decreasing the number of Type I and type II error)
       Requires :
        CSV with average feature distance for each feature between to category given by "main.py exportStats"
        see requirements of "main.py exportStats"

       Step of the assignment
       -----------------------
        Optimizing Weight

       Command
       -------
        main.py optimisedWeigth

       Parameters
       ----------
        None

       Returns/Output
       --------------
        Print the optimal weight for each features in the command line and the average distance for each category to another using those weight
        The optimal weight is the weight maximizing the objective function regarding the constraints given"""
    if sys.argv[1] == "optimisedWeigth":
        lp.optimisedWeight()

if len(sys.argv) == 3:

    """Display a 3D mesh

       Step of the assignment
       -----------------------
        Step 1

       Command
       -------
        main.py render

       Parameters
       ----------
        filepath : The path of the mesh to display

       Returns/Output
       --------------
        Open a windows showing the mesh located at <filepath> """
    if sys.argv[1] == "render":
        m = Mesh(sys.argv[2])
        m.render()

    """Print property of a 3D mesh

       Step of the assignment
       -----------------------
        Step 2

       Command
       -------
        main.py analyze

       Parameters
       ----------
        filepath : The path of the file to analyze

       Returns/Output
       --------------
        Print properties of the given 3D mesh in the command line """
    if sys.argv[1] == "analyze":
        m = Mesh(sys.argv[2])
        data = m.dataFilter()
        for key in data:
            print(key + " : " + str(data[key]))

    """Export properties of all 3D mesh of the database given as parameter
       May requires :
        Normalized database located at <OUTPUT FOLDER>/NormaliseDB/ given by "main.py full-normalisation"
       Step of the assignment
       -----------------------
        Step 2

       Command
       -------
        main.py statistics

       Parameters
       ----------
        DB : "original" or "normalized"

       Returns/Output
       --------------
        Export a CSV containing properties of each object of the database given in parameter
        Return a list of dictionnary representing each row of the csv"""
    if sys.argv[1] == "statistics":
        if sys.argv[2]=="original" or sys.argv[2]=="normalized":
            db.exportDBProp(sys.argv[2] == "original")

    """Export histogram of the data given in parameter based on the data save by "main.py statistics <DB>"
        Requires :
        A CSV containing properties of each object of the database given in parameter to "main.py statistics <DB>"
        See requirements of statistics command
        
       Step of the assignment
       -----------------------
       Step 2

       Command
       -------
       main.py histograms

       Parameters
       ----------
       dataName : a dataName value (contained in the enumerated class dataName)

       Returns/Output
       --------------
       Export histogram of the data given in parameter in ./output/histograms """
    if sys.argv[1] == "histograms":
        db.histograms(sys.argv[2])

    """Normalizing a folder (i.e. a category) of the database

       Step of the assignment
       -----------------------
       Step 3

       Command
       -------
       main.py category-normalisation

       Parameters
       ----------
       folderName : name of the folder in the database to normalize

       Returns/Output
       --------------
       Export normalized 3d mesh of the folder in the <OUTPUT FOLDER>/NormaliseDB/<folderName> """
    if sys.argv[1] == "category-normalisation":
        db.normCategory(sys.argv[2])

    """Export histogram of the feature given in parameter based on the data save by "main.py features"
       Requires :
        None

       Step of the assignment
       -----------------------
        Step 4

       Command
       -------
        main.py histogram-features

       Parameters
       ----------
        featureName : a featureName value (contained in the enumerated class featureName)

       Returns/Output
       --------------
        Export histogram of the feature given in parameter in ./output/histograms """
    if sys.argv[1] == "histogram-features":
        db.drawCategoryFeatures(sys.argv[2])

    """ Export a distance matrix from one object to each other in the normalize database
        Requires :
        A CSV containing features extracted from each object of the database (exported by "main.py features")
        See requirements of "main.py features"

        Step of the assignment
        -----------------------
        Debug features (Step 4)
        used for TSNE (Step 5)

        Command
        -------
        main.py distanceMatrix

        Parameters
        ----------
        distanceFunction : "emd" or "euclidean"

        Returns/Output
        --------------
        Return a list containing for each object a dictionary containing the path of a mesh as key and the distance to it as value
        Export a distance matrix from one object to each other in the normalize database """
    if sys.argv[1] == "distanceMatrix":
        db.exportDistanceMatrix(sys.argv[2])

    """Reduct the features to a 2D features vector based ont the distance matrix based between the N-dimensionnal vector
       Requires :
        distanceMatrix given by "main.py distanceMatrix <distanceFunction>"
        See requirements of "main.py distanceMatrix <distanceFunction>"

       Step of the assignment
       -----------------------
        Step 5

       Command
       -------
        main.py tsne

       Parameters
       ----------
        distanceFunction : "emd" or "euclidean"

       Returns/Output
       --------------
        Show a 2D plot with each points colored according to their category to visualise if the clustering looks good """
    if sys.argv[1] == "tsne":
        distMatrix, rowLabel = db.parseDistMatrix(sys.argv[2])
        tsne(distMatrix, rowLabel, 100000)

    """Compute the average feature distance for each feature between categories using <distanceFunction> distance type
       Requires :
        distanceMatrix given by "main.py distanceMatrix <distanceFunction>"
        See requirements of "main.py distanceMatrix <distanceFunction>"

       Step of the assignment
       -----------------------
        Optimizing Weight

       Command
       -------
        main.py exportStats

       Parameters
       ----------
        distanceFunction : "emd" or "euclidean"

       Returns/Output
       --------------
        Export a CSV with the average feature distance for each feature from a category to another (for each unique unordered pair of category) """
    if sys.argv[1] == "exportStats":
        for key in featureName.featureWeight:
            featureName.featureWeight[key] = 1
        resAvg, resStd = db.exportFeaturesDist(sys.argv[2])

if len(sys.argv) == 4:

    """Show all 20 object of a category from the same POV to visually check the normalisation step
       Requires :
        Normalized database located at <OUTPUT FOLDER>/NormaliseDB/ given by "main.py full-normalisation"
       
       Step of the assignment
       -----------------------
       Debug features (Step 3)

       Command
       -------
       main.py view-category

       Parameters
       ----------
       folderName : name of the folder in the database to check
       DB : Indicate if the original or the normalized database should be used

       Returns/Output
       --------------
       Export an image showing all 20 object in a 5 by 4 canvas from same POV to <OUTPUT FOLDER>/NormaliseDB/<folderName>/meshes_overview.jpg
       show the plot if DEBUG from settings is True
       Side effects
       ------------
       Export image for each object of the category a thumbnail from same POV in <OUTPUT FOLDER>/NormaliseDB/<folderName>/screenshot"""
    if sys.argv[1] == "view-category":
        if sys.argv[3] == "original" or sys.argv[3] == "normalized":
            db.viewCategory(sys.argv[2], sys.argv[3]=="original")

    """Query for the k most similar object in the normalised database
       Requires :
        Normalized database located at <OUTPUT FOLDER>/NormaliseDB/ given by "main.py full-normalisation"
         
       Step of the assignment
       -----------------------
       Step 4

       Command
       -------
       main.py query

       Parameters
       ----------
       filepath : path of the mesh of the query
       k : Number of mesh wanted in the result

       Returns/Output
       --------------
       Show in a plot the k most similar object
       
       Side effects
       ------------
       Save screenshot of the query mesh and the result in <OUTPUT FOLDER>/screenshot/
       Show the 4 most similar object in a pyplot windows (used for illustration purpose in the report) """
    if sys.argv[1] == "query":
        queryRes = db.query(sys.argv[2], "euclidean", k=int(sys.argv[3]))
        db.exportQueryRes(sys.argv[2], queryRes)

    """Query for the k most similar object in the normalised database
       Requires:
        Normalized database located at <OUTPUT FOLDER>/NormaliseDB/ given by "main.py full-normalisation"
        
       Step of the assignment
       -----------------------
       Step 4

       Command
       -------
       main.py annQuery

       Parameters
       ----------
       filepath : path of the mesh of the query 
       k : Number of mesh wanted in the result
        
       Returns/Output
       --------------
       Show in a plot the k most similar object

       Side effects
       ------------
       Building the tree and querying the k most similar object in this tree using ANN
       Save screenshot of the query mesh and the result in <OUTPUT FOLDER>/screenshot/
       Show the 4 most similar object in a pyplot windows (used for illustration purpose in the report) """
    if sys.argv[1] == "annQuery":
        tree, rowLabel = db.buildTree() # leaf_size = 4
        queryRes = db.annQuery(sys.argv[2], int(sys.argv[3]), tree, rowLabel)
        db.exportQueryRes(sys.argv[2], queryRes)
__author__ = 'jimrutt'

def  ontology_setup():

    OBJECTS = atomspace.add_node(types.ConceptNode, "Objects",TRUTH_VALUE)
    GAMEOBJECTS = atomspace.add_node(types.ConceptNode, "GameObjects",TRUTH_VALUE)
    VISIONOBJECTS = atomspace.add_node(types.ConceptNode, "VisionObjects",TRUTH_VALUE)
    ATTRIBUTES = atomspace.add_node(types.ConceptNode, "Attributes",TRUTH_VALUE)

    COLORS = atomspace.add_node(types.ConceptNode, "Colors",TRUTH_VALUE)
    BLUE = atomspace.add_node(types.ConceptNode, "Blue",TRUTH_VALUE)
    RED = atomspace.add_node(types.ConceptNode, "Red",TRUTH_VALUE)
    GREEN = atomspace.add_node(types.ConceptNode, "Green",TRUTH_VALUE)
    BROWN = atomspace.add_node(types.ConceptNode, "Brown",TRUTH_VALUE)

    TYPES = atomspace.add_node(types.ConceptNode, "Types",TRUTH_VALUE)
    ROCK = atomspace.add_node(types.ConceptNode, "Rock",TRUTH_VALUE)
    SHRUB = atomspace.add_node(types.ConceptNode, "Shrub",TRUTH_VALUE)
    TREE = atomspace.add_node(types.ConceptNode, "Tree",TRUTH_VALUE)
    RABBIT = atomspace.add_node(types.ConceptNode, "Rabbit",TRUTH_VALUE)
    WOLF = atomspace.add_node(types.ConceptNode, "Wolf",TRUTH_VALUE)
    DEER  = atomspace.add_node(types.ConceptNode, "Deer",TRUTH_VALUE)

    SIZES = atomspace.add_node(types.ConceptNode, "Sizes",TRUTH_VALUE)
    SMALL = atomspace.add_node(types.ConceptNode, "Small",TRUTH_VALUE)
    MEDIUM = atomspace.add_node(types.ConceptNode, "Medium",TRUTH_VALUE)
    LARGE = atomspace.add_node(types.ConceptNode, "Large",TRUTH_VALUE)

    LOCATIONS = atomspace.add_node(types.ConceptNode, "Locations",TRUTH_VALUE)
    GLOBALXY = atomspace.add_node(types.ConceptNode, "GlobalXY",TRUTH_VALUE)
    TIMES = atomspace.add_node(types.ConceptNode, "Times",TRUTH_VALUE)
    EPISODE1 = atomspace.add_node(types.ConceptNode, "Episode1",TRUTH_VALUE)

    COLORSLIST = [BLUE,RED,GREEN,BROWN]
    TYPESLIST = [ROCK,SHRUB,TREE,RABBIT,WOLF,DEER]
    SIZESLIST = [SMALL,MEDIUM,LARGE]

    build_ontology = \
    '''
    (InheritanceLink (ConceptNode "GameObjects") (ConceptNode "Objects"))
    (InheritanceLink (ConceptNode "VisualObjects") (ConceptNode "GameObjects"))
    (InheritanceLink (ConceptNode "Colors") (ConceptNode "Attributes"))
    (InheritanceLink (ConceptNode "Types") (ConceptNode "Attributes"))
    (InheritanceLink (ConceptNode "Sizes") (ConceptNode "Attributes"))
    (InheritanceLink (ConceptNode "Blue") (ConceptNode "Colors"))
    (InheritanceLink (ConceptNode "Red") (ConceptNode "Colors"))
    (InheritanceLink (ConceptNode "Green") (ConceptNode "Colors"))
    (InheritanceLink (ConceptNode "Brown") (ConceptNode "Colors"))
    (InheritanceLink (ConceptNode "Rock") (ConceptNode "Types"))
    (InheritanceLink (ConceptNode "Shrub") (ConceptNode "Types"))
    (InheritanceLink (ConceptNode "Tree") (ConceptNode "Types"))
    (InheritanceLink (ConceptNode "Rabbit") (ConceptNode "Types"))
    (InheritanceLink (ConceptNode "Wolf") (ConceptNode "Types"))
    (InheritanceLink (ConceptNode "Deer") (ConceptNode "Types"))
    (InheritanceLink (ConceptNode "Small") (ConceptNode "Sizes"))
    (InheritanceLink (ConceptNode "Medium") (ConceptNode "Sizes"))
    (InheritanceLink (ConceptNode "Large") (ConceptNode "Sizes"))
    (InheritanceLink (ConceptNode "GlobalXY") (ConceptNode "Locations"))
    (InheritanceLink (ConceptNode "Episode1") (ConceptNode "Times"))
    '''
    result = scheme_eval_h(atomspace, build_ontology)

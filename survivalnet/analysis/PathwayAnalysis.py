import numpy as np
from .RiskCohort import RiskCohort
from .SSGSEA import SSGSEA
from .Visualization import _FixSymbols
from .Visualization import RankedBar
from .Visualization import RankedBox
from .Visualization import PairScatter
from .Visualization import KMPlots


def PathwayAnalysis(Model, Normalized, Symbols, SetNames, Sets,
                    Survival, Censored, Alpha=0, GSEANormalize=False,
                    NPlot=10, Path=None):
    """
    Pathway-based analysis of model sensitivity to inputs. Used with models
    trained on pure gene expression features. Transforms risk gradients of
    features obtained from backpropagation into pathway enrichment scores.

    Parameters:
    -----------
    Model : class
    Model class instance generated by finetuned training.

    Normalized : array_like
    Numpy array containing normalized feature values used in training /
    finetuning. These features will be mapped to gene pathways and should
    populate the pathways densely, as with whole-exome RNA sequencing.
    Features are in columns and samples are in rows.

    Symbols : array_like
    List containing strings describing features. These symbols should be
    harmonized with those used in the genesets for mapping between the two.

    SetNames : array_like
    List of strings containing gene set names.

    Sets : array_like
    List of lists with each containing the gene symbols for one gene set.

    Survival : array_like
    Array containing death or last followup values.

    Censored : array_like
    Array containing vital status at last followup. 1 (alive) or 0 (deceased).

    NPlot : scalar
    Number of features to include when generating boxplot.
    Features are scored by absolute mean gradient and the highest N magnitude
    features will be used to generate the plot. Default value = 10.

    Path : string
    Path to store .pdf versions of plots generated.
    """

    # wrap long gene set names and remove leading and trailing whitespace
    CorrectedSetNames, Types = _FixSymbols(SetNames)

    # trim gene symbols names
    CorrectedSymbols = [Symbol[0:str.rfind(str(Symbol), '_')]
                        for Symbol in Symbols]

    # generate risk derivative profiles for cohort
    print "Generting risk gradient profiles..."
    Gradients = RiskCohort(Model, Normalized)

    # perform GSEA on mean feature risk profiles
    ES = np.squeeze(SSGSEA(np.median(Gradients, axis=0)[np.newaxis, :],
                           CorrectedSymbols, Sets, Alpha, False))

    # re-order pathways by mean absolute enrichment score
    Order = np.argsort(-np.abs(ES))
    cSetNames = [CorrectedSetNames[i] for i in Order]
    cTypes = Types
    cES = ES[Order]

    # generate ranked bar plot
    print "Generating mean enrichment score bar plot..."
    BarFig = RankedBar(cES[0:NPlot],
                       [cSetNames[i] for i in np.arange(NPlot)],
                       [cTypes[i] for i in np.arange(NPlot)],
                       XLabel='Pathway',
                       YLabel='Enrichment Score')

    # perform SSGSEA on feature risk gradient profiles
    SSES = SSGSEA(Gradients, CorrectedSymbols, Sets, Alpha, GSEANormalize)

    # re-order single-sample enrichment scores
    cSSES = SSES[:, Order]

    # generate ranked box plot series
    print "Generating single-sample enrichment boxplot..."
    BoxFig = RankedBox(cSSES[:, 0:NPlot],
                       [cSetNames[i] for i in np.arange(NPlot)],
                       [cTypes[i] for i in np.arange(NPlot)],
                       XLabel='Pathway',
                       YLabel='Single-Sample Enrichment Score')

    # generate paired scatter plot for gradients
    print "Generating single-sample enrichment scatter plots..."
    PSGradFig = PairScatter(cSSES[:, 0:NPlot],
                            [cSetNames[i] for i in np.arange(NPlot)],
                            [cTypes[i] for i in np.arange(NPlot)])

    # generate Kaplan-Meier plots for individual features
    print "Generating single-sample enrichment Kaplan-Meier plots..."
    KMFigs = KMPlots(cSSES[:, 0:NPlot], cSSES[:, 0:NPlot],
                     [cSetNames[i] for i in np.arange(NPlot)],
                     [cTypes[i] for i in np.arange(NPlot)],
                     Survival, Censored)

    # save figures
    print "Saving figures..."
    if Path is not None:

        # save standard figures
        BarFig.savefig(Path + 'Pathway.Bar.pdf')
        BoxFig.savefig(Path + 'Pathway.Box.pdf')
        PSGradFig.savefig(Path + 'Pathway.PairedScatter.pdf')
        for i, Figure in enumerate(KMFigs):
            Figure.savefig(Path + 'Pathway.KM.' +
                           SetNames[Order[i]] + '.pdf')
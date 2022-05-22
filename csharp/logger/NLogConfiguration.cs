//#########################################################################################################
//# NLog config: https://github.com/nlog/NLog/wiki/Configuration-API
//#########################################################################################################

using NLog;
using NLog.Config;
using NLog.Targets;

namespace NoobChain
{

    /// <summary>
    /// Programmatic configuration of NLog in order to support logfile at runtime
    /// </summary>
    class NLogConfiguration
    {
        internal static void Configure(string logFilePath)
        {
            // Create configuration object 
            var config = new LoggingConfiguration();

            // Create targets and add them to the configuration
            var consoleTarget = new ColoredConsoleTarget();
            config.AddTarget("console", consoleTarget);

            var fileTarget = new FileTarget();
            config.AddTarget("file", fileTarget);

            // Set target properties 
            //consoleTarget.Layout = @"${date:format=HH\:mm\:ss} ${logger} ${message}";
            consoleTarget.Layout = @"${message}";
            fileTarget.FileName = logFilePath;
            fileTarget.Layout = "${message}";

            //  Define rules
            var rule1 = new LoggingRule("*", LogLevel.Debug, consoleTarget);
            config.LoggingRules.Add(rule1);

            var rule2 = new LoggingRule("*", LogLevel.Debug, fileTarget);
            config.LoggingRules.Add(rule2);

            // Activate the configuration
            LogManager.Configuration = config;
        }
    }
}
